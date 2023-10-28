from typing import Any

import psycopg_pool

from event_handler.db.interface import Database, DatabaseEntry, DatabaseEntryKey


class Postgresql(Database):  # skip: coverage
    """A class that represents a PostgreSQL database connection."""

    def __init__(self, host: str, port: int, db_name: str, user_name: str, password: str):
        """Initialize the connection pool with the given parameters."""
        conninfo = f"host={host} port={port} dbname={db_name} user={user_name} password={password}"
        self._pool = psycopg_pool.AsyncConnectionPool(conninfo=conninfo, open=False)
        self._is_connected = False

    async def connect(self):
        """Open the connection pool and return self."""
        await self._pool.open()
        self._is_connected = True

    def is_connected(self) -> bool:
        return self._is_connected

    async def disconnect(self):
        """Close the connection pool."""
        await self._pool.close()
        self._is_connected = False

    async def create_table_if_not_exists(self, table_name: str, schema: str):
        """Create a table with the given name and schema if it does not exist."""
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});"

        async with self._pool.connection(timeout=5) as conn:
            await conn.execute(query)

    async def insert_data(self, table_name: str, data: DatabaseEntry) -> DatabaseEntryKey:
        """Insert a row of data into the table and return the primary key."""
        placeholders = ", ".join(["?" for _ in data.keys()])
        columns = ", ".join(data.keys())
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES({placeholders}) RETURNING id;"

        async with self._pool.connection() as conn:
            return await conn.execute(query, values)

    async def replace_data(self, table_name: str, data: DatabaseEntry) -> DatabaseEntryKey:
        """Replace a row of data into the table and return the primary key."""
        placeholders = ", ".join(["?" for _ in data.keys()])
        columns = ", ".join(data.keys())
        values = tuple(data.values())
        query = f"REPLACE INTO {table_name} ({columns}) VALUES({placeholders});"

        async with self._pool.connection() as conn:
            return await conn.execute(query, values)

    async def delete_data_by_key_and_value(self, table_name: str, key: str, value: Any):
        query = f"DELETE FROM {table_name} WHERE {key}='{value}';"

        async with self._pool.connection() as conn:
            cursor = await conn.execute(query)
            return await cursor.fetchall()

    async def select_all_data(self, table_name: str) -> list[DatabaseEntry]:
        """Select all rows of data from the table and return a list of entries."""
        query = f"SELECT FROM {table_name}'"

        async with self._pool.connection() as conn:
            cursor = await conn.execute(query)
            return await cursor.fetchall()

    async def select_all_data_by_key_and_value(self, table_name: str, key: str, value: Any) -> list[DatabaseEntry]:
        """Select all rows from the table that match the given key and value and return a list of entries."""
        query = f"SELECT FROM {table_name} WHERE {key}='{value}';"

        async with self._pool.connection() as conn:
            cursor = await conn.execute(query)
            return await cursor.fetchall()
