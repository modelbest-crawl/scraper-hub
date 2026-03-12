from __future__ import annotations

import os
import random

from packages.utils.config import load_config


class ProxyPool:
    def __init__(self, project_name: str | None = None) -> None:
        self._project_name = project_name
        self._proxies: list[str] = []
        self._bad_proxies: set[str] = set()
        self._load()

    def _load(self) -> None:
        proxies: list[str] = []
        if self._project_name:
            config = load_config(self._project_name)
            proxies = config.get("proxies", [])
        env_proxies = os.environ.get("SCRAPER_PROXIES", "")
        if env_proxies:
            proxies.extend(p.strip() for p in env_proxies.split(",") if p.strip())
        self._proxies = [p for p in proxies if p not in self._bad_proxies]

    def get(self) -> str | None:
        if not self._proxies:
            return None
        return random.choice(self._proxies)

    def remove(self, proxy: str) -> None:
        self._bad_proxies.add(proxy)
        self._proxies = [p for p in self._proxies if p != proxy]

    def refresh(self) -> None:
        self._bad_proxies.clear()
        self._load()
