import threading
import time


class RateLimiter:
    def __init__(self, rate: float = 1.0, max_burst: int = 5) -> None:
        self.rate = rate
        self.max_burst = max_burst
        self._tokens = float(max_burst)
        self._last_update = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_update
        self._tokens = min(
            self.max_burst,
            self._tokens + elapsed * self.rate,
        )
        self._last_update = now

    def acquire(self) -> None:
        while True:
            with self._lock:
                self._refill()
                if self._tokens >= 1:
                    self._tokens -= 1
                    return
                wait_time = (1 - self._tokens) / self.rate
                self._tokens = 0
                self._last_update = time.monotonic()
            time.sleep(wait_time)

    def __enter__(self) -> "RateLimiter":
        self.acquire()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        pass
