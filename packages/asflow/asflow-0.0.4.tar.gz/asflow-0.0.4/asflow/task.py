import asyncio
import contextlib
import contextvars
import hashlib
import inspect
import os
import threading
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

    class Canceled(Exception):
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
        if flow_progress := self.flow.run._progress:
            desc = desc or self.run.encode_params()
            description = self.flow.run.TASKRUN_FORMAT.format(desc=desc)
            return TaskProgress(flow_progress, description, **kwargs)
        else:
            raise RuntimeError("progress disabled")

    def write(self, data):
        run = self.run
        if run.canceled:
            raise Task.Canceled()
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
        retry_on_exceptions=(Exception,),
        ignore_on_exceptions=(),
        skip_on_exceptions=(),
    ):
        self.task = task
        self.limit = limit if limit is not None else os.cpu_count()
        self.retry = retry
        self.retry_on_exceptions = retry_on_exceptions
        self.ignore_on_exceptions = ignore_on_exceptions
        self.skip_on_exceptions = skip_on_exceptions

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
        # Check async
        is_async = False
        if asyncio.iscoroutinefunction(func):
            # async def functions
            is_async = True
        elif callable(func) and asyncio.iscoroutinefunction(func.__call__):
            # async callable object like joblib.memory.AsyncMemorizedFunc
            is_async = True

        # Semaphore
        if self.limit:
            if is_async:
                self.semaphore = asyncio.BoundedSemaphore(self.limit)
            else:
                self.semaphore = threading.BoundedSemaphore(self.limit)
        else:
            self.semaphore = None

        # retry
        match self.retry:
            case None:

                def retry(func):
                    return func
            case int():
                retry = Retry(total=self.retry, exceptions=self.retry_on_exceptions)
            case Retry():
                retry = self.retry
            case _:
                raise TypeError(self.retry)

        if is_async:

            @wraps(func)
            @retry
            async def async_task_wrapper(*args, **kwargs):
                try:
                    async with TaskRun(self, func, args, kwargs) as run:
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
            @retry
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
class TaskRun(contextlib.AbstractContextManager, contextlib.AbstractAsyncContextManager):
    config: TaskConfig
    func: Callable
    args: list[Any]
    kwargs: dict[Any, Any]

    canceled: bool = False

    @property
    def flow(self):
        return self.config.task.flow

    def cancel(self):
        self.canceled = True

    def encode_params(self):
        args = [str(x) for x in self.args]
        kwargs = [f"{k}={v}" for k, v in self.kwargs.items()]
        return ", ".join(args + kwargs)

    def __str__(self):
        return f"{self.func.__name__}({self.encode_params()})"

    def get_hash(self):
        return hashlib.md5(str(self).encode()).hexdigest()

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

    @cached_property
    def output_path(self):
        if self.config.location:
            return Path(self.config.location.format(**self.context))

    # AbstractContextManager

    def __enter__(self):
        self._stack = contextlib.ExitStack()

        # Task tacking
        if flow_run := self.flow.run:
            self._stack.enter_context(flow_run.track_task(self))

        if self.output_path:
            if self.output_path.exists():
                # Use exception here to exit from a context manager
                raise Task.Skipped()

        # Limit concurrency
        if self.config.semaphore:
            self._stack.enter_context(self.config.semaphore)

        # Start logging after acquiring semaphore
        self._stack.enter_context(self._logging_context())

        if self.output_path:
            self._enter_output_context(self.output_path)

        # Exception handling
        self._stack.enter_context(self._exception_context())

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._stack.__exit__(exc_type, exc_val, exc_tb)

    def _enter_output_context(self, path):
        self._stack.enter_context(self._delete_context(path))
        self.writer = self._stack.enter_context(self.config.compressor.writer(path))

    @contextlib.contextmanager
    def _track_task_context(self, flow_run):
        flow_run.track_task_start(self)
        try:
            yield
        finally:
            flow_run.track_task_finish(self)

    @contextlib.contextmanager
    def _logging_context(self):
        start = time.time()
        yield
        end = time.time()
        duration = end - start

        if self.flow.verbose:
            self.flow.console.log(f"Task {self} finished in {duration:.2f}s")

    @contextlib.contextmanager
    def _delete_context(self, path):
        try:
            yield
        except BaseException:
            # Delete incomplete files on exceptions
            # Note: Catch BaseException here to handle KeyboardInterrupt, etc.
            if path.exists():
                path.unlink()
            raise

    @contextlib.contextmanager
    def _exception_context(self):
        try:
            yield
        except tuple(self.config.ignore_on_exceptions) as exc:
            self.flow.console.log(f"Ignoring {exc.__class__.__name__}: {exc}")
            raise Task.Skipped() from None
        except tuple(self.config.skip_on_exceptions):
            pass

    # AbstractAsyncContextManager

    async def __aenter__(self):
        self._stack = contextlib.AsyncExitStack()

        # Task tacking
        if flow_run := self.flow.run:
            self._stack.enter_context(flow_run.track_task(self))

        if self.output_path:
            if self.output_path.exists():
                # Use exception here to exit from a context manager
                raise Task.Skipped()

        # Limit concurrency
        if self.config.semaphore:
            await self._stack.enter_async_context(self.config.semaphore)

        # Start logging after acquiring semaphore
        self._stack.enter_context(self._logging_context())

        if self.output_path:
            self._enter_output_context(self.output_path)

        # Exception handling
        self._stack.enter_context(self._exception_context())

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._stack.__aexit__(exc_type, exc_val, exc_tb)
