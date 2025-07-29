"""SQLite cache backend."""

import sqlite3 as sql
from dataclasses import dataclass, field
from pathlib import Path

from tacobi.data_source.cache import CacheBackend
from tacobi.data_source.encode import EncodedDataType


def default_db_path() -> Path:
    """Generate a default path to the SQLite database."""
    return Path.cwd() / "cache.db"


@dataclass
class SQLiteCache(CacheBackend):
    """A cache backend that uses a SQLite database to store and retrieve data."""

    db_path: Path = field(default_factory=default_db_path)
    """The path to the SQLite database."""

    _conn: sql.Connection | None = None
    """The SQLite connection."""

    # Init and cleanup

    def __post_init__(self) -> None:
        """Initialize the SQLite connection.

        Create the cache table if it doesn't exist.
        """
        self._conn = sql.connect(self.db_path)
        self._conn.row_factory = sql.Row

        cursor = self._conn.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS cache (
            key TEXT PRIMARY KEY,
            data BLOB
        )"""
        )

    def __del__(self) -> None:
        """Close the SQLite connection."""
        self.close()

    # Cache Operations

    async def get(self, key: str) -> EncodedDataType | None:
        """Get the data for the given key.

        ### Arguments
        - key: The key to get the data for.

        ### Returns
        - The data for the given key, or None if the data is not found.
        """
        if not self._conn:
            msg = "SQLite connection not initialized"
            raise RuntimeError(msg)

        cursor = self._conn.cursor()
        cursor.execute("SELECT data FROM cache WHERE key = ?", (key,))
        result = cursor.fetchone()
        return result[0] if result else None

    async def set(self, key: str, value: EncodedDataType) -> None:
        """Set the data for the given key.

        ### Arguments
        - key: The key to set the data for.
        - data: The data to set.
        """
        if not self._conn:
            msg = "SQLite connection not initialized"
            raise RuntimeError(msg)

        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO cache (key, data)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET data = excluded.data
        """,
            (key, value),
        )
        self._conn.commit()

    async def clear(self) -> None:
        """Clear the cache."""
        if not self._conn:
            msg = "SQLite connection not initialized"
            raise RuntimeError(msg)

        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM cache")
        self._conn.commit()

    def close(self) -> None:
        """Close the SQLite connection."""
        if self._conn:
            self._conn.close()

    async def cleanup(self) -> None:
        """Cleanup the cache."""
        self.close()
