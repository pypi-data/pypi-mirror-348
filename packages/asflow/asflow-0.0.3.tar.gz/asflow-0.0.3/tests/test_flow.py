import asyncio
import tempfile

import pytest

from asflow.flow import AsyncFlowRun, Flow


@pytest.fixture
def flow():
    with tempfile.TemporaryDirectory() as name:
        yield Flow(name)


async def test_sync_flow_error(flow):
    with pytest.raises(AssertionError):

        @flow
        def flow1():
            pass


async def test_flow(flow):
    @flow.task
    def task1(msg):
        return msg

    @flow.task
    async def task2(msg):
        return msg.upper()

    @flow
    async def flow1(msg):
        assert type(flow.run) is AsyncFlowRun

        return await task2(task1(msg))

    assert asyncio.iscoroutinefunction(flow1)
    assert await flow1("ok") == "OK"
