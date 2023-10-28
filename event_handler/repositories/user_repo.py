from event_handler.db.interface import Database
from event_handler.models.user import User, UserId, UserWithId

Schema = str


class UserRepository:
    """A class that represents a repository for users in a database."""

    def __init__(self, db: Database):
        """Initializes the UserRepository with a Database object.

        Args:
            db (Database): The database object that handles the connection and queries.
        """
        self._db = db

    @property
    def _table_name(self) -> str:
        """Returns the name of the table that stores the users.

        Returns:
            str: The name of the table.
        """
        return "Users"

    @property
    def _schema(self) -> Schema:
        """Returns the schema of the table that stores the users.

        Returns:
            Schema: The schema of the table.
        """
        return (
            "id integer NOT NULL PRIMARY KEY AUTOINCREMENT,"
            "first_name varchar(255) NOT NULL,"
            "last_name varchar(255) NOT NULL,"
            "email varchar(255) NOT NULL"
        )

    async def create_repository(self):
        """Creates the table for users if it does not exist in the database."""
        await self._db.create_table_if_not_exists(table_name=self._table_name, schema=self._schema)

    async def create_user(self, user: User) -> UserId:
        """Inserts a new user into the database and returns its id.

        Args:
            user (User): The user object to be inserted.

        Returns:
            UserId: The id of the inserted user.
        """
        id = await self._db.insert_data(table_name=self._table_name, data=user.__dict__)
        return id[0]

    async def get_user(self, id: UserId) -> UserWithId | None:
        """Retrieves a user from the database by its id.

        Args:
            id (UserId): The id of the user to be retrieved.

        Returns:
            User | None: The user object if found, or None otherwise.
        """
        user = await self._db.select_all_data_by_key_and_value(table_name=self._table_name, key="id", value=id)
        if len(user) == 1:  # there is only one entry associated per id
            return UserWithId(id=user[0][0], first_name=user[0][1], last_name=user[0][2], email=user[0][3])

    async def delete_user(self, id: UserId):
        """Deletes a user from the database by its id.

        Args:
            id (UserId): The id of the user to be deleted.
        """
        await self._db.delete_data_by_key_and_value(table_name=self._table_name, key="id", value=id)
