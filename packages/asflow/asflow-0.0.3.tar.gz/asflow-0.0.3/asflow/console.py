import threading

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
        self._live = rich.live.Live(self._table, console=self._console)

    def enter_live_context(self, stack):
        if not self._live.is_started:
            return stack.enter_context(self._live)
