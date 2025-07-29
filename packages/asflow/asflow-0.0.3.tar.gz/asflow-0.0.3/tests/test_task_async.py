import asyncio
import tempfile

import pytest

from asflow.flow import Flow
from asflow.retry import Retry
from asflow.task import AsyncTaskRun


@pytest.fixture
def flow():
    with tempfile.TemporaryDirectory() as name:
        yield Flow(name)


async def test_async_task(flow):
    @flow.task
    async def task1(msg):
        assert type(flow.task.run) is AsyncTaskRun
        return msg

    assert asyncio.iscoroutinefunction(task1)
    assert await task1("OK") == "OK"


async def test_async_task_call(flow):
    @flow.task()
    async def task1(msg):
        assert type(flow.task.run) is AsyncTaskRun
        return msg

    assert asyncio.iscoroutinefunction(task1)
    assert await task1("OK") == "OK"


async def test_async_task_retry(flow):
    @flow.task(retry=0)
    async def task1():
        task1.called += 1
        raise RuntimeError()

    task1.called = 0
    with pytest.raises(RuntimeError):
        await task1()
    assert task1.called == 1


async def test_async_task_retry_object(flow):
    @flow.task(retry=Retry(total=3, backoff_factor=0.0, backoff_jitter=0.0))
    async def task1():
        task1.called += 1
        raise RuntimeError()

    task1.called = 0
    with pytest.raises(RuntimeError):
        await task1()
    assert task1.called == 4


async def test_async_task_retry_errors(flow):
    @flow.task()
    async def task1():
        raise RuntimeError()

    with pytest.raises(RuntimeError):
        await task1()

    with pytest.raises(TypeError):

        @flow.task(retry="bad")
        def task1():
            pass


async def test_async_task_on(flow):
    @flow.task(on="test")
    async def task1(msg):
        flow.task.write(msg)

    await task1("OK")
    assert flow.path("test").read_text() == "OK"


async def test_async_task_limit(flow):
    @flow.task(limit=1)
    async def task1(msg):
        return msg

    assert await task1("OK") == "OK"
