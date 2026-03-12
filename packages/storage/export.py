import csv
import json
from pathlib import Path
from typing import Any

import pandas as pd


def export_csv(items: list[dict[str, Any]], filepath: str) -> None:
    if not items:
        return
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)


def export_json(
    items: list[dict[str, Any]],
    filepath: str,
    indent: int = 2,
) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=indent, ensure_ascii=False)


def export_excel(
    items: list[dict[str, Any]],
    filepath: str,
    sheet_name: str = "Sheet1",
) -> None:
    if not items:
        return
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(items)
    df.to_excel(path, sheet_name=sheet_name, index=False)
