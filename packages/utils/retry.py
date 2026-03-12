import functools
import time
from typing import Callable, ParamSpec, TypeVar

from loguru import logger

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: BaseException | None = None
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Retry {attempt}/{max_attempts} for {func.__name__} "
                            f"after {e.__class__.__name__}: {e}"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        raise
            raise last_exc or RuntimeError("Retry exhausted")

        return wrapper

    return decorator
