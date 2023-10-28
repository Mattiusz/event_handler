from functools import lru_cache

from pydantic_settings import BaseSettings

from event_handler.db.interface import Database
from event_handler.db.postgresql import Postgresql
from event_handler.db.sqlite import Sqlite


class SqliteSettings(BaseSettings):
    """A class to store the settings for SQLite database."""

    db_path: str = ":memory"
    """The path to the SQLite database file. Default is in-memory."""


class PostgresSettings(BaseSettings):
    """A class to store the settings for PostgreSQL database."""

    host: str = "127.0.0.1"
    """The host name or IP address of the PostgreSQL server. Default is localhost."""

    port: int = 5432
    """The port number of the PostgreSQL server. Default is 5432."""

    db_name: str = "event_handler"
    """The name of the database to connect to."""

    user_name: str = ""
    """The user name to authenticate with the PostgreSQL server."""

    password: str = ""
    """The password to authenticate with the PostgreSQL server."""


class GeneralSettings(BaseSettings):
    """A class to store the general settings for the application."""

    use_postgres: bool = False
    """A flag to indicate whether to use PostgreSQL or SQLite as the database. Default is False."""

    request_timeout_in_s: float = 5
    """The timeout in seconds for HTTP requests. Default is 5."""


@lru_cache()
def get_sqlite_settings() -> SqliteSettings:
    """A function to get the SQLite settings from the environment variables.

    Returns:
        SqliteSettings: An instance of SqliteSettings class.
    """
    return SqliteSettings()


@lru_cache()
def get_postgres_settings() -> PostgresSettings:
    """A function to get the PostgreSQL settings from the environment variables.

    Returns:
        PostgresSettings: An instance of PostgresSettings class.
    """
    return PostgresSettings()


@lru_cache()
def get_general_settings() -> GeneralSettings:
    """A function to get the general settings from the environment variables.

    Returns:
        GeneralSettings: An instance of GeneralSettings class.
    """
    return GeneralSettings()


@lru_cache()
def get_database() -> Database:
    """A function to get a database instance based on the general settings.

    Returns:
        Database: An instance of Database class, either Postgresql or Sqlite.
    """
    if get_general_settings().use_postgres:
        settings = get_postgres_settings()
        return Postgresql(
            host=settings.host,
            port=settings.port,
            db_name=settings.db_name,
            user_name=settings.user_name,
            password=settings.password,
        )

    settings = get_sqlite_settings()
    return Sqlite(path=settings.db_path)
