import asyncio
import contextlib
import contextvars
import hashlib
import inspect
import os
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property, wraps
from pathlib import Path
from typing import Any

from .compressor import create_compressor
from .retry import Retry
from .serializer import create_serializer


class TaskProgress:
    def __init__(self, progress, *args, **kwargs):
        self.progress = progress
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        self.task_id = self.progress.add_task(*self.args, **self.kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.remove_task(self.task_id)

    def advance(self, advance=1):
        self.progress.advance(self.task_id, advance)

    def update(self, **kwargs):
        self.progress.update(self.task_id, **kwargs)


class Task:
    run_var = contextvars.ContextVar("@task")

    class Skipped(Exception):
        pass

    def __init__(self, flow):
        self.flow = flow

    def __call__(self, func=None, **kwargs):
        if func is None:
            # @flow.task(**kwargs)
            return TaskConfig(self, **kwargs).decorator
        else:
            # @flow.task
            return TaskConfig(self).decorator(func)

    @property
    def run(self):
        return Task.run_var.get()

    def progress(self, desc=None, **kwargs):
        if flow_progress := self.flow.run.progress:
            description = self.flow.run.TASKRUN_FORMAT.format(desc=desc or self.run)
            return TaskProgress(flow_progress, description, **kwargs)
        else:
            raise RuntimeError("progress disabled")

    def write(self, data):
        run = self.run
        run.writer.write(run.config.serializer.encode(data))


class TaskConfig:
    def __init__(
        self,
        task,
        on=None,
        serializer=None,
        compressor=None,
        limit=None,
        retry=None,
    ):
        self.task = task

        # writer
        if on:
            self.location = self.normalize_location(on)
            path = Path(self.location)
            self.serializer = create_serializer(path, serializer)
            self.compressor = create_compressor(path, compressor)
        else:
            self.location = None
            self.serializer = None
            self.compressor = None

        # limit
        if limit is None:
            limit = os.cpu_count()
        if limit:
            self.semaphore = asyncio.Semaphore(limit)
        else:
            self.semaphore = None

        # retry
        match retry:
            case None:
                self.retry = lambda func: func
            case int():
                self.retry = Retry(total=retry)
            case Retry():
                self.retry = retry
            case _:
                raise TypeError(retry)

    def normalize_location(self, pattern: str) -> str:
        if "://" in pattern:
            raise NotImplementedError(pattern)

        path = self.task.flow.path(pattern)

        # Replace "*" by "{hash}"
        match path.name.count("*"):
            case 0:
                pass
            case 1:
                path = path.with_name(path.name.replace("*", "{hash}"))
            case _:
                raise ValueError("too many wildcard", pattern)

        # Make sure the parent directory exists
        # Note: Executed at loading time to catch errors earlier
        path.parent.mkdir(parents=True, exist_ok=True)

        return str(path)

    def decorator(self, func):
        assert callable(func)

        # Check async
        is_async = False
        if asyncio.iscoroutinefunction(func):
            # async def functions
            is_async = True
        elif callable(func) and asyncio.iscoroutinefunction(func.__call__):
            # joblib.memory.AsyncMemorizedFunc
            is_async = True

        if is_async:

            @wraps(func)
            @self.retry
            async def async_task_wrapper(*args, **kwargs):
                try:
                    async with AsyncTaskRun(self, func, args, kwargs) as run:
                        token = Task.run_var.set(run)
                        try:
                            return await func(*args, **kwargs)
                        finally:
                            Task.run_var.reset(token)
                except Task.Skipped:
                    pass

            return async_task_wrapper
        else:

            @wraps(func)
            @self.retry
            def task_wrapper(*args, **kwargs):
                try:
                    with TaskRun(self, func, args, kwargs) as run:
                        token = Task.run_var.set(run)
                        try:
                            return func(*args, **kwargs)
                        finally:
                            Task.run_var.reset(token)
                except Task.Skipped:
                    pass

            return task_wrapper


@dataclass
class TaskRun(contextlib.AbstractContextManager):
    config: TaskConfig
    func: Callable
    args: list[Any]
    kwargs: dict[Any, Any]

    @property
    def flow(self):
        return self.config.task.flow

    @cached_property
    def context(self):
        context = {}

        # hash
        if "{hash}" in self.config.location:
            context["hash"] = self.get_hash()

        # function parameters
        sig = inspect.signature(self.func)
        bound = sig.bind(*self.args, **self.kwargs)
        bound.apply_defaults()
        for key, val in bound.arguments.items():
            context[key] = val

        return context

    def get_hash(self):
        args = [repr(x) for x in self.args]
        kwargs = [k + "=" + repr(v) for k, v in self.kwargs]
        funcall = f"{self.func.__name__}({', '.join(args + kwargs)})"
        return hashlib.md5(funcall.encode()).hexdigest()

    @cached_property
    def output_path(self):
        if self.config.location:
            return Path(self.config.location.format(**self.context))

    def __str__(self):
        args = [repr(x) for x in self.args]
        kwargs = [k + "=" + repr(v) for k, v in self.kwargs]
        return f"{self.func.__name__}({', '.join(args + kwargs)})"

    def __enter__(self):
        self._stack = contextlib.ExitStack()
        if self.output_path:
            if self.output_path.exists():
                raise Task.Skipped()
            self.enter_common_contexts()
            self.enter_output_contexts(self.output_path)
        else:
            self.enter_common_contexts()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._stack.__exit__(exc_type, exc_val, exc_tb)

    def enter_common_contexts(self):
        self._stack.enter_context(self.flow_progress())
        self._stack.enter_context(self.task_logging())

    def enter_output_contexts(self, path):
        self._stack.enter_context(self.delete_on_exception(path))
        self.writer = self._stack.enter_context(self.config.compressor.writer(path))

    @contextlib.contextmanager
    def flow_progress(self):
        if flow_run := self.flow.run:
            flow_run.add_task(self)
            yield
            flow_run.remove_task(self)
        else:
            yield

    @contextlib.contextmanager
    def task_logging(self):
        start = time.time()
        yield
        end = time.time()
        duration = end - start

        if self.flow.run and self.flow.run.config.verbose:
            self.flow.progress.console.log(f"Task {self} finished in {duration:.2f}s")

    @contextlib.contextmanager
    def delete_on_exception(self, path):
        try:
            yield
        except BaseException:
            # Delete incomplete files on exceptions
            # Note: Catch BaseException here to handle KeyboardInterrupt, etc.
            if path.exists():
                path.unlink()
            raise


class AsyncTaskRun(TaskRun, contextlib.AbstractAsyncContextManager):
    async def __aenter__(self):
        self._stack = contextlib.AsyncExitStack()
        if self.output_path:
            if self.output_path.exists():
                raise Task.Skipped()
            await self.enter_common_async_contexts()
            self.enter_output_contexts(self.output_path)
        else:
            await self.enter_common_async_contexts()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._stack.__aexit__(exc_type, exc_val, exc_tb)

    async def enter_common_async_contexts(self):
        # Start progress tacking
        self._stack.enter_context(self.flow_progress())

        # Limit concurrency
        if self.config.semaphore:
            await self._stack.enter_async_context(self.config.semaphore)

        # Start logging after acquiring semaphore
        self._stack.enter_context(self.task_logging())
