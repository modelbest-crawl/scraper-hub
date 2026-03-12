from __future__ import annotations


class ScraperError(Exception):
    """Base exception for all scraper-related errors."""

    pass


class FetchError(ScraperError):
    """Raised when HTTP request fails."""

    pass


class ParseError(ScraperError):
    """Raised when parsing fails."""

    pass


class StorageError(ScraperError):
    """Raised when storage operations fail."""

    pass


class RateLimitError(ScraperError):
    """Raised when rate limited by target."""

    pass


class AntiDetectError(ScraperError):
    """Raised when blocked by anti-scraping measures."""

    pass
