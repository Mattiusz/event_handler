from typing import Any

import aiosqlite

from event_handler.db.interface import Database, DatabaseEntry, DatabaseEntryKey


class Sqlite(Database):
    """A class that represents a SQLite database connection."""

    def __init__(self, path: str):
        """Initialize the connection object with the given path."""
        self._path = path
        self._conn: aiosqlite.Connection = None
        self._is_connected = False

    async def connect(self):
        """Connect to the database and set the connection attribute."""
        self._conn = await aiosqlite.connect(self._path)
        self._is_connected = True

    def is_connected(self) -> bool:
        return self._is_connected

    async def disconnect(self):
        """Close the connection to the database."""
        await self._conn.close()
        self._is_connected = False

    async def create_table_if_not_exists(self, table_name: str, schema: str):
        """Create a table with the given name and schema if it does not exist."""
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});"

        await self._conn.execute(query)
        await self._conn.commit()

    async def _get_last_rowid_and_commit(self):
        """Get the last inserted row id and commit the changes."""
        query = "SELECT last_insert_rowid();"
        cursor = await self._conn.execute(query)
        await self._conn.commit()
        data = await cursor.fetchone()
        return data

    async def insert_data(self, table_name: str, data: DatabaseEntry) -> DatabaseEntryKey:
        """Insert a row of data into the table and return the primary key."""
        # Insert data
        placeholders = ", ".join(["?" for _ in data.keys()])
        columns = ", ".join(data.keys())
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES({placeholders});"
        await self._conn.execute(query, values)

        # Get id of inserted entry
        return await self._get_last_rowid_and_commit()

    async def replace_data(self, table_name: str, data: DatabaseEntry):
        """Replace a row of data into the table and return the primary key."""
        # Replace data
        placeholders = ", ".join(["?" for _ in data.keys()])
        columns = ", ".join(data.keys())
        values = tuple(data.values())
        query = f"REPLACE INTO {table_name} ({columns}) VALUES({placeholders});"
        await self._conn.execute(query, values)

    async def delete_data_by_key_and_value(self, table_name: str, key: str, value: Any):
        """Delete a row of data from the table that matches the given key and value."""
        query = f"DELETE FROM {table_name} WHERE {key}='{value}';"

        await self._conn.execute(query)
        await self._conn.commit()

    async def select_all_data(self, table_name: str) -> list[DatabaseEntry]:
        """Select all rows of data from the table and return a list of tuples."""
        query = f"SELECT * FROM {table_name};"

        cursor = await self._conn.execute(query)
        return await cursor.fetchall()

    async def select_all_data_by_key_and_value(self, table_name: str, key: str, value: Any) -> list[DatabaseEntry]:
        """Select all rows of data from the table that match the given key and value and return a list of tuples."""
        query = f"SELECT * FROM {table_name} WHERE {key}='{value}';"

        cursor = await self._conn.execute(query)
        await self._conn.commit()
        return await cursor.fetchall()
