import asyncio
import random
import time


class Retry:
    def __init__(
        self,
        total: int = 10,
        backoff_factor: float = 0.0,
        backoff_jitter: float = 1.0,
        exceptions=(Exception,),
    ):
        self.total = total
        self.backoff_factor = backoff_factor
        self.backoff_jitter = backoff_jitter
        self.exceptions = exceptions

    def _sleep_time(self, attempt):
        base = self.backoff_factor * (2**attempt)
        jitter = random.uniform(0, self.backoff_jitter)
        return base + jitter

    def __call__(self, func):
        if asyncio.iscoroutinefunction(func):

            async def async_wrapper(*args, **kwargs):
                for attempt in range(self.total + 1):
                    try:
                        return await func(*args, **kwargs)
                    except self.exceptions:
                        if attempt == self.total:
                            raise
                        await asyncio.sleep(self._sleep_time(attempt))

            return async_wrapper
        else:

            def sync_wrapper(*args, **kwargs):
                for attempt in range(self.total + 1):
                    try:
                        return func(*args, **kwargs)
                    except self.exceptions:
                        if attempt == self.total:
                            raise
                        time.sleep(self._sleep_time(attempt))

            return sync_wrapper
