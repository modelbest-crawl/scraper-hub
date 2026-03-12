from __future__ import annotations

import time
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from packages.core.exceptions import AntiDetectError, RateLimitError
from packages.http.fingerprint import get_chrome_headers
from packages.http.proxy_pool import ProxyPool


class HttpClient:
    def __init__(
        self,
        proxy_enabled: bool = False,
        rate_limit: float = 1.0,
        max_retries: int = 3,
        timeout: float = 30.0,
        project_name: str | None = None,
    ) -> None:
        self._proxy_enabled = proxy_enabled
        self._rate_limit = rate_limit
        self._max_retries = max_retries
        self._timeout = timeout
        self._project_name = project_name
        self._proxy_pool = ProxyPool(project_name) if proxy_enabled else None
        self._last_request_time: float = 0.0

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        self._session = requests.Session()
        self._session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        self._session.mount("http://", HTTPAdapter(max_retries=retry_strategy))

    def _apply_rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < self._rate_limit:
            time.sleep(self._rate_limit - elapsed)
        self._last_request_time = time.monotonic()

    def _get_proxies(self) -> dict[str, str] | None:
        if not self._proxy_enabled or not self._proxy_pool:
            return None
        proxy = self._proxy_pool.get()
        if proxy:
            return {"http": proxy, "https": proxy}
        return None

    def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> requests.Response:
        self._apply_rate_limit()
        headers = kwargs.pop("headers", {}) or {}
        base_headers = get_chrome_headers()
        headers = {**base_headers, **headers}
        kwargs.setdefault("timeout", self._timeout)
        kwargs.setdefault("headers", headers)
        proxies = self._get_proxies()
        if proxies:
            kwargs["proxies"] = proxies

        response = self._session.request(method, url, **kwargs)

        if response.status_code == 429:
            if self._proxy_pool and proxies:
                self._proxy_pool.remove(proxies.get("http", ""))
            raise RateLimitError(f"Rate limited: {url}")

        if response.status_code in (403, 418, 503) and "blocked" in response.text.lower():
            if self._proxy_pool and proxies:
                self._proxy_pool.remove(proxies.get("http", ""))
            raise AntiDetectError(f"Blocked by anti-scraping: {url}")

        return response

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        return self._request("POST", url, **kwargs)
