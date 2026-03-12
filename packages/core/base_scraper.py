from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from packages.core.exceptions import FetchError, ParseError, ScraperError, StorageError
from packages.http.client import HttpClient
from packages.utils.config import load_config, get_target_urls
from packages.utils.logger import get_logger


class BaseScraper(ABC):
    def __init__(self, project_name: str) -> None:
        self._project_name = project_name
        self._config = load_config(project_name)
        self._logger = get_logger(project_name)
        self._http = HttpClient(
            proxy_enabled=self._config.get("proxy_enabled", False),
            rate_limit=self._config.get("rate_limit", 1.0),
            max_retries=self._config.get("max_retries", 3),
            timeout=self._config.get("timeout", 30.0),
            project_name=project_name,
        )

    def get_target_urls(self) -> list[str]:
        return get_target_urls(self._project_name)

    @abstractmethod
    def fetch(self, url: str) -> Any:
        pass

    @abstractmethod
    def parse(self, raw_data: Any) -> list[Any]:
        pass

    @abstractmethod
    def save(self, items: list[Any]) -> None:
        pass

    def notify_error(self, e: Exception) -> None:
        self._logger.error(f"Scraper error: {e}")

    def run(self) -> None:
        urls = self.get_target_urls()
        if not urls:
            self._logger.warning("No target URLs configured")
            return

        for url in urls:
            try:
                self._logger.info(f"Fetching {url}")
                raw_data = self.fetch(url)
                items = self.parse(raw_data)
                self.save(items)
                self._logger.info(f"Saved {len(items)} items from {url}")
            except FetchError as e:
                self._logger.error(f"Fetch failed: {e}")
                self.notify_error(e)
            except ParseError as e:
                self._logger.error(f"Parse failed: {e}")
                self.notify_error(e)
            except StorageError as e:
                self._logger.error(f"Storage failed: {e}")
                self.notify_error(e)
            except ScraperError as e:
                self._logger.error(f"Scraper error: {e}")
                self.notify_error(e)
            except Exception as e:
                self._logger.exception(f"Unexpected error: {e}")
                self.notify_error(e)
