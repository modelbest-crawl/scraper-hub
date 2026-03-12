import json
from pathlib import Path
from typing import Any


class CookieManager:
    def __init__(
        self,
        domain: str,
        storage_dir: str = "cookies",
        max_age_seconds: int = 86400,
    ) -> None:
        self.domain = domain
        self.storage_dir = Path(storage_dir)
        self.max_age_seconds = max_age_seconds
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._cookie_path = self.storage_dir / f"{domain}.json"

    def save(self, cookies: dict[str, Any]) -> None:
        with open(self._cookie_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2)

    def load(self) -> dict[str, Any]:
        if not self._cookie_path.exists():
            return {}
        with open(self._cookie_path, encoding="utf-8") as f:
            return json.load(f)

    def is_expired(self) -> bool:
        if not self._cookie_path.exists():
            return True
        age = self._cookie_path.stat().st_mtime
        import time

        return (time.time() - age) > self.max_age_seconds

    def clear(self) -> None:
        if self._cookie_path.exists():
            self._cookie_path.unlink()
