"""Console script for event_handler"""
import os
import sys

import click
import uvicorn
from fastapi import FastAPI

from event_handler.api import config, events, users
from event_handler.logger import logger


def print_environment():
    logger.info(f"API_HOST: {os.environ.get('API_HOST', '')}")
    logger.info(f"API_PORT: {os.environ.get('API_PORT', '')}")
    logger.info(f"POSTGRESQL_HOST: {os.environ.get('POSTGRESQL_HOST', '')}")
    logger.info(f"USE_POSTGRES: {os.environ.get('USE_SIMULATION', '')}")
    logger.info(f"POSTGRESQL_HOST: {os.environ.get('POSTGRESQL_HOST', '')}")
    logger.info(f"POSTGRESQL_PORT: {os.environ.get('USE_SIMULATION', '')}")
    logger.info(f"POSTGRESQL_DB_NAME: {os.environ.get('POSTGRESQL_HOST', '')}")
    logger.info(f"POSTGRESQL_USER_NAME: {os.environ.get('POSTGRESQL_USER_NAME', '')}")
    logger.info(f"POSTGRESQL_PASSWORD: {os.environ.get('POSTGRESQL_PASSWORD', '')}")
    logger.info(f"SQLITE_PATH: {os.environ.get('SQLITE_PATH')}")


def set_environment():
    general_settings = config.get_general_settings()
    general_settings.use_postgres = os.environ.get("POSTGRESQL_HOST", "false") == "true"

    postgres_settings = config.get_postgres_settings()
    postgres_settings.host = os.environ.get("POSTGRESQL_HOST", "127.0.0.1")
    postgres_settings.port = int(os.environ.get("POSTGRESQL_PORT", 5432))
    postgres_settings.db_name = os.environ.get("POSTGRESQL_DB_NAME", "event_handler")
    postgres_settings.user_name = os.environ.get("POSTGRESQL_USER_NAME", "")
    postgres_settings.password = os.environ.get("POSTGRESQL_PASSWORD", "")

    sqlite_settings = config.get_sqlite_settings()
    sqlite_settings.db_path = os.environ.get("SQLITE_PATH", ":memory:")


def start_server():
    app = FastAPI()

    app.include_router(events.router)
    app.include_router(users.router)

    uvicorn.run(
        app, host=os.environ.get("API_HOST", "localhost"), port=int(os.environ.get("API_PORT", 8000)), log_config=None
    )


@click.command()
def main():
    """Console script for event_handler"""
    print_environment()
    set_environment()
    start_server()
    return 0


if __name__ == "__main__":
    sys.exit(main())
