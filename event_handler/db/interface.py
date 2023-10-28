from abc import ABCMeta, abstractmethod
from typing import Any

DatabaseEntry = dict[str, Any]
DatabaseEntryKey = int


class Database(metaclass=ABCMeta):  # skip: coverage
    """An abstract base class for a relational database."""

    @abstractmethod
    async def connect(self):
        """Connects to the database."""
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        """Checks if the database is connected."""
        ...

    @abstractmethod
    async def disconnect(self):
        """Disconnects from the database."""
        ...

    @abstractmethod
    async def create_table_if_not_exists(self, table_name: str, schema: str):
        """Creates a table in the database if it does not exist.

        Args:
            table_name (str): The name of the table to create.
            schema (str): The schema of the table as a string.
        """
        ...

    @abstractmethod
    async def insert_data(self, table_name: str, data: DatabaseEntry) -> DatabaseEntryKey:
        """Inserts data into a table in the database.

        Args:
            table_name (str): The name of the table to insert data into.
            data (DatabaseEntry): The data to insert as a DatabaseEntry object.

        Returns:
            Any: The associated database key
        """
        ...

    @abstractmethod
    async def replace_data(self, table_name: str, data: DatabaseEntry):
        """Replaces data in a table in the database.

        Args:
            table_name (str): The name of the table to replace data in.
            data (DatabaseEntry): The data to replace as a DatabaseEntry object.
        """
        ...

    @abstractmethod
    async def delete_data_by_key_and_value(self, table_name: str, key: str, value: Any):
        """Deletes data from a table in the database by key and value.

        Args:
            table_name (str): The name of the table to select data from.
            key (str): The key to filter data by.
            value (Any): The value to filter data by.
        """
        ...

    @abstractmethod
    async def select_all_data(self, table_name: str) -> list[DatabaseEntry]:
        """Selects all data from a table in the database.

        Args:
            table_name (str): The name of the table to select data from.
            key (str): The key to filter data by.
            value (Any): The value to filter data by.

        Returns:
            list[DatabaseEntry]: A list of DatabaseEntry objects
        """
        ...

    @abstractmethod
    async def select_all_data_by_key_and_value(self, table_name: str, key: str, value: Any) -> DatabaseEntry:
        """Selects data from a table in the database by key and value.

        Args:
            table_name (str): The name of the table to select data from.
            key (str): The key to filter data by.
            value (Any): The value to filter data by.

        Returns:
            list[DatabaseEntry]: A list of DatabaseEntry objects that match the filter criteria.
        """
        ...
