from contextlib import contextmanager
from pathlib import Path


class Compressor:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class NoCompressor(Compressor):
    @contextmanager
    def writer(self, path: Path):
        with path.open("wb") as f:
            yield f


class GzipCompressor(Compressor):
    @contextmanager
    def writer(self, path: Path):
        import gzip

        with gzip.GzipFile(path, "wb", **self.kwargs) as f:
            yield f


class ZstdCompressor(Compressor):
    @contextmanager
    def writer(self, path: Path):
        import zstandard

        with path.open("wb") as f:
            with zstandard.ZstdCompressor(**self.kwargs).stream_writer(f) as writer:
                yield writer


def create_compressor(path, compressor):
    if isinstance(compressor, Compressor):
        return compressor

    compressor = compressor or {}
    match path.suffix:
        case ".gz":
            return GzipCompressor(**compressor)
        case ".zst":
            return ZstdCompressor(**compressor)
        case _:
            return NoCompressor()
