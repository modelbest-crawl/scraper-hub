import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()


class HeartbeatReporter:
    def __init__(self, project_name: str, notifier: Any = None) -> None:
        self.project_name = project_name
        self.notifier = notifier
        self._storage_dir = Path(
            os.getenv("HEARTBEAT_STORAGE_DIR", ".heartbeat_reports")
        )
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._report_path = self._storage_dir / f"{project_name}.jsonl"

    def report(
        self,
        status: str,
        count: int,
        elapsed: float,
        error: str | None = None,
    ) -> None:
        record = {
            "project": self.project_name,
            "status": status,
            "count": count,
            "elapsed": elapsed,
            "error": error,
        }
        with open(self._report_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        if self.notifier and hasattr(self.notifier, "send"):
            msg = f"[{self.project_name}] {status} | count={count} | elapsed={elapsed:.1f}s"
            if error:
                msg += f" | error={error}"
            self.notifier.send(msg)
