import json
from pathlib import Path
from typing import Any


class FileStore:
    def __init__(self, base_dir: str) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, filename: str) -> Path:
        return self.base_dir / filename

    def save_json(self, data: dict[str, Any], filename: str) -> None:
        with open(self._path(filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def save_jsonl(self, items: list[dict[str, Any]], filename: str) -> None:
        with open(self._path(filename), "w", encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    def load_json(self, filename: str) -> dict[str, Any]:
        path = self._path(filename)
        if not path.exists():
            return {}
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def load_jsonl(self, filename: str) -> list[dict[str, Any]]:
        path = self._path(filename)
        if not path.exists():
            return []
        items: list[dict[str, Any]] = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
        return items
