import asyncio
import contextlib
import contextvars
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any

from .console import Console
from .task import Task


@dataclass(kw_only=True)
class TaskState:
    task_id: str
    total: int


class Flow:
    run_var = contextvars.ContextVar("@flow", default=None)

    def __init__(
        self,
        base: str | Path = ".",
        verbose: bool = False,
    ):
        self.base = Path(base)
        self.verbose = verbose
        self.console = Console.get_instance()
        self.task = Task(self)

    @property
    def run(self):
        return Flow.run_var.get()

    def path(self, pathlike):
        return self.base / pathlike

    def __call__(self, func=None, **kwargs):
        if func is None:
            # @flow(**kwargs)
            return FlowConfig(self, **kwargs).decorator
        else:
            # @flow
            return FlowConfig(self, **kwargs).decorator(func)


@dataclass
class FlowConfig:
    flow: Flow
    progress: bool = True

    def decorator(self, func):
        assert asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def async_flow_wrapper(*args, **kwargs):
            async with FlowRun(self, func, args, kwargs) as run:
                token = Flow.run_var.set(run)
                try:
                    return await func(*args, **kwargs)
                finally:
                    Flow.run_var.reset(token)

        return async_flow_wrapper


@dataclass
class FlowRun(contextlib.AbstractAsyncContextManager):
    config: FlowConfig
    func: Callable
    args: list[Any]
    kwargs: dict[Any, Any]

    FLOW_FORMAT = "[blue]@flow[/] {flow}()"
    TASK_FORMAT = " [blue]@task[/] {task}()"
    TASKRUN_FORMAT = "       {desc}"

    async def __aenter__(self):
        self._stack = contextlib.ExitStack()
        self._task_runs = []

        if self.config.progress:
            # Add flow progress
            description = self.FLOW_FORMAT.format(flow=self.func.__name__)
            self._progress = self.config.flow.console.add_progress()
            self._progress_task_id = self._progress.add_task(description, start=False)
            self._progress_tasks = {}

            # Live start
            self.config.flow.console.live_start(self)
        else:
            self._progress = None

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cancel all running tasks
        if exc_type == asyncio.exceptions.CancelledError:
            for run in self._task_runs:
                run.cancel()

        # Stop flow progress
        if self.config.progress:
            if exc_type is None:
                self._progress.update(self._progress_task_id, total=0, completed=0)
                self._progress.stop_task(self._progress_task_id)

        # Live stop
        self.config.flow.console.live_stop(self)

        return self._stack.__exit__(exc_type, exc_val, exc_tb)

    @contextlib.contextmanager
    def track_task(self, task_run):
        self._track_task_start(task_run)
        try:
            yield
        finally:
            self._track_task_finish(task_run)

    def _track_task_start(self, task_run):
        self._task_runs.append(task_run)

        # Create a progress task for each task function
        # Increment the total count by each task_run
        if self._progress:
            if task_state := self._progress_tasks.get(task_run.func):
                task_state.total += 1
                self._progress.update(task_state.task_id, total=task_state.total)
            else:
                description = self.TASK_FORMAT.format(task=task_run.func.__name__)
                task_id = self._progress.add_task(description, total=1)
                self._progress_tasks[task_run.func] = TaskState(task_id=task_id, total=1)

    def _track_task_finish(self, task_run):
        if self._progress:
            task_state = self._progress_tasks[task_run.func]
            self._progress.advance(task_state.task_id)
