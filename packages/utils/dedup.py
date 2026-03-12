import json
from pathlib import Path


class Deduplicator:
    def __init__(self, storage_path: str = ".dedup_cache") -> None:
        self._path = Path(storage_path)
        self._path.mkdir(parents=True, exist_ok=True)
        self._cache_path = self._path / "seen.json"
        self._seen: set[str] = self._load()

    def _load(self) -> set[str]:
        if not self._cache_path.exists():
            return set()
        with open(self._cache_path, encoding="utf-8") as f:
            data = json.load(f)
        return set(data.get("keys", []))

    def _save(self) -> None:
        with open(self._cache_path, "w", encoding="utf-8") as f:
            json.dump({"keys": list(self._seen)}, f)

    def is_seen(self, key: str) -> bool:
        return key in self._seen

    def mark_seen(self, key: str) -> None:
        self._seen.add(key)
        self._save()

    def clear(self) -> None:
        self._seen.clear()
        if self._cache_path.exists():
            self._cache_path.unlink()
