from __future__ import annotations

from typing import Any

try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None

_DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

_ua: UserAgent | None = None


def _get_ua() -> UserAgent | None:
    global _ua
    if _ua is None and UserAgent is not None:
        try:
            _ua = UserAgent()
        except Exception:
            pass
    return _ua


def get_random_ua() -> str:
    ua = _get_ua()
    if ua is not None:
        try:
            return ua.random
        except Exception:
            pass
    return _DEFAULT_UA


def get_chrome_headers() -> dict[str, str]:
    return {
        "User-Agent": get_random_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }


def get_mobile_headers() -> dict[str, str]:
    return {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
