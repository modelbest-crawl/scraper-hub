import os
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

load_dotenv()


class DatabaseStore:
    def __init__(self, url: str | None = None) -> None:
        self._url = url or os.getenv("DATABASE_URL", "sqlite:///./scraper.db")
        self._engine: Engine = create_engine(self._url)

    def execute(self, sql: str, params: dict[str, Any] | None = None) -> None:
        with self._engine.connect() as conn:
            conn.execute(text(sql), params or {})
            conn.commit()

    def insert_many(self, table: str, items: list[dict[str, Any]]) -> None:
        if not items:
            return
        columns = list(items[0].keys())
        cols_str = ", ".join(columns)
        placeholders = ", ".join(f":{c}" for c in columns)
        sql = f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders})"
        with self._engine.connect() as conn:
            for item in items:
                conn.execute(text(sql), item)
            conn.commit()

    def query(self, sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        with self._engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            rows = result.fetchall()
            if not rows:
                return []
            columns = result.keys()
            return [dict(zip(columns, row)) for row in rows]
