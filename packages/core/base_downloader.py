from __future__ import annotations

import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import requests

from packages.http.fingerprint import get_chrome_headers


class BaseDownloader(ABC):
    def __init__(self, project_name: str) -> None:
        self._project_name = project_name

    @abstractmethod
    def get_download_urls(self) -> list[tuple[str, str]]:
        pass

    def download_one(
        self,
        url: str,
        filename: str,
        output_dir: str | Path,
        max_retries: int = 3,
    ) -> Path | None:
        output_path = Path(output_dir) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        for attempt in range(max_retries):
            try:
                headers = get_chrome_headers()
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=60,
                    stream=True,
                )
                response.raise_for_status()
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return output_path
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return None
        return None

    def download_all(
        self,
        output_dir: str | Path,
        max_workers: int = 4,
    ) -> list[Path | None]:
        urls = self.get_download_urls()
        results: list[Path | None] = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.download_one, url, filename, output_dir): (url, filename)
                for url, filename in urls
            }
            for future in as_completed(futures):
                results.append(future.result())
        return results
