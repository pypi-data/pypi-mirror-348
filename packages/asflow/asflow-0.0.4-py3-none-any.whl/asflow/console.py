import threading
from functools import wraps

import rich
import rich.console
import rich.live
import rich.progress
import rich.table


class Console:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance

    def __init__(self, stderr=True):
        # The container of progress output
        self._table = rich.table.Table(show_header=False, show_edge=False, pad_edge=False)

        # The output goes to stderr
        self._console = rich.console.Console(stderr=stderr)

        # The live display controller
        self._live = rich.live.Live(self._table, console=self._console, transient=True)
        self._live_runs = []

    def live_start(self, run):
        if len(self._live_runs) == 0:
            self._live.start(refresh=True)
        self._live_runs.append(run)

    def live_stop(self, run):
        self._live_runs.remove(run)
        if len(self._live_runs) == 0:
            self._live.stop()

    def add_progress(self):
        progress = rich.progress.Progress()
        self._table.add_row(progress)
        return progress

    @wraps(rich.console.Console.log)
    def log(self, *args, **kwargs):
        self._console.log(*args, **kwargs)

    @wraps(rich.console.Console.print)
    def print(self, *args, **kwargs):
        self._console.print(*args, **kwargs)
