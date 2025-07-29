import asyncio
import contextlib
import contextvars
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any

import rich.progress

from .console import Console
from .task import Task


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
        if "verbose" not in kwargs:
            kwargs["verbose"] = self.verbose

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
    verbose: bool = False

    def decorator(self, func):
        assert asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def async_flow_wrapper(*args, **kwargs):
            async with AsyncFlowRun(self, func, args, kwargs) as run:
                token = Flow.run_var.set(run)
                try:
                    return await func(*args, **kwargs)
                finally:
                    Flow.run_var.reset(token)

        return async_flow_wrapper


@dataclass
class TaskState:
    task_id: str
    total: int


@dataclass
class AsyncFlowRun:
    config: FlowConfig
    func: Callable
    args: list[Any]
    kwargs: dict[Any, Any]

    FLOW_FORMAT = "[blue]@flow[/] {flow}()"
    TASK_FORMAT = " [blue]@task[/] {task}()"
    TASKRUN_FORMAT = "       {desc}"

    async def __aenter__(self):
        self._stack = contextlib.ExitStack()

        if self.config.progress:
            description = self.FLOW_FORMAT.format(flow=self.func.__name__)
            self.progress = rich.progress.Progress(transient=True)
            self.progress.add_task(description, start=False)
            self.running_tasks = {}

            self.config.flow.console.enter_live_context(self._stack)
            self.config.flow.console._table.add_row(self.progress)
        else:
            self.progress = None

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self._stack.__exit__(exc_type, exc_val, exc_tb)

    def add_task(self, task_run):
        if self.progress:
            func = task_run.func
            if state := self.running_tasks.get(func):
                state.total += 1
                self.progress.update(state.task_id, total=state.total)
            else:
                description = self.TASK_FORMAT.format(task=func.__name__)
                task_id = self.progress.add_task(description, total=1)
                self.running_tasks[func] = TaskState(task_id=task_id, total=1)

    def remove_task(self, task_run):
        if self.progress:
            state = self.running_tasks[task_run.func]
            self.progress.advance(state.task_id)
