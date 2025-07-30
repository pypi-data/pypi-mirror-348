import inspect
import tempfile

import pytest

from asflow.flow import Flow
from asflow.retry import Retry
from asflow.task import TaskRun


@pytest.fixture
def flow():
    with tempfile.TemporaryDirectory() as name:
        yield Flow(name)


def test_sync_task(flow):
    @flow.task
    def task1(msg):
        assert type(flow.task.run) is TaskRun
        return msg

    assert inspect.isfunction(task1)
    assert task1("OK") == "OK"


def test_sync_task_call(flow):
    @flow.task()
    def task1(msg):
        assert type(flow.task.run) is TaskRun
        return msg

    assert inspect.isfunction(task1)
    assert task1("OK") == "OK"


def test_sync_task_retry(flow):
    @flow.task(retry=0)
    def task1():
        task1.called += 1
        raise RuntimeError()

    task1.called = 0
    with pytest.raises(RuntimeError):
        task1()
    assert task1.called == 1


def test_sync_task_retry_object(flow):
    @flow.task(retry=Retry(total=3, backoff_factor=0.0, backoff_jitter=0.0))
    def task1():
        task1.called += 1
        raise RuntimeError()

    task1.called = 0
    with pytest.raises(RuntimeError):
        task1()
    assert task1.called == 4


def test_sync_task_retry_errors(flow):
    @flow.task()
    def task1():
        raise RuntimeError()

    with pytest.raises(RuntimeError):
        task1()

    with pytest.raises(TypeError):

        @flow.task(retry="bad")
        def task1():
            pass


async def test_sync_task_progress(flow):
    @flow.task()
    def task1(total):
        with flow.task.progress(total=total) as progress:
            for _ in range(total):
                progress.advance()
            return total

    @flow
    async def flow1(total):
        return task1(total)

    result = await flow1(100)
    assert result == 100


def test_sync_task_txt(flow):
    @flow.task(on="t1/test.txt")
    def task1(msg):
        flow.task.write(msg)

    task1("OK")
    assert flow.path("t1/test.txt").read_text() == "OK"


def test_sync_task_txt_gz(flow):
    import gzip

    @flow.task(on="t1/test.txt.gz")
    def task1(msg):
        flow.task.write(msg)

    task1("OK")
    with gzip.GzipFile(flow.path("t1/test.txt.gz")) as f:
        assert f.read().decode() == "OK"


def test_sync_task_txt_zst(flow):
    import zstandard

    @flow.task(on="t1/test.txt.zst")
    def task1(msg):
        flow.task.write(msg)

    task1("OK")
    with flow.path("t1/test.txt.zst").open("rb") as f:
        reader = zstandard.ZstdDecompressor().stream_reader(f)
        assert reader.read().decode() == "OK"
