from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


class Pipeline:
    def __init__(self) -> None:
        self._steps: list[Callable[[T], T]] = []

    def add_step(self, fn: Callable[[T], T]) -> "Pipeline":
        self._steps.append(fn)
        return self

    def run(self, items: T) -> T:
        result = items
        for step in self._steps:
            result = step(result)
        return result
