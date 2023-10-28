import asyncio

from fastapi import APIRouter, Depends, Response, status
from typing_extensions import Annotated

from event_handler.api.config import GeneralSettings, get_database, get_general_settings
from event_handler.db.interface import Database
from event_handler.logger import logger
from event_handler.models.user import User, UserId, UserKey, UserWithId
from event_handler.repositories.user_repo import UserRepository

router = APIRouter(prefix="/api/v1.0/users", tags=["users"], responses={404: {"description": "Not found"}})


async def get_repository(database: Annotated[Database, Depends(get_database)]) -> UserRepository:
    if not database.is_connected():
        await database.connect()
    repo = UserRepository(db=database)
    await repo.create_repository()
    return repo


@router.put(
    "/create_user",
    status_code=status.HTTP_200_OK,
    response_model=UserKey,
    responses={
        status.HTTP_200_OK: {"description": "User successfully created"},
        status.HTTP_408_REQUEST_TIMEOUT: {"description": "Request timed out."},
    },
)
async def create_user(
    user: User,
    response: Response,
    settings: Annotated[GeneralSettings, Depends(get_general_settings)],
    repo: Annotated[UserRepository, Depends(get_repository)],
):
    try:
        id = await asyncio.wait_for(repo.create_user(user), settings.request_timeout_in_s)
        logger.info("Created user at id={id}.")
        return {"id": str(id)}
    except asyncio.TimeoutError:
        logger.error("Timeout while calling create_user().")
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT


@router.put(
    "/get_user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserWithId | None,
    responses={
        status.HTTP_200_OK: {"description": "User successfully created."},
        status.HTTP_404_NOT_FOUND: {"description": "User not found."},
        status.HTTP_408_REQUEST_TIMEOUT: {"description": "Request timed out."},
    },
)
async def get_user(
    user_id: UserId,
    response: Response,
    settings: Annotated[GeneralSettings, Depends(get_general_settings)],
    repo: Annotated[UserRepository, Depends(get_repository)],
):
    try:
        user = await asyncio.wait_for(repo.get_user(user_id), settings.request_timeout_in_s)
        if user is not None:
            return user.__dict__
        else:
            logger.error(f"User with id={user_id}) not found.")
            response.status_code = status.HTTP_404_NOT_FOUND
    except asyncio.TimeoutError:
        logger.error(f"Timeout while calling get_user(id={user_id}).")
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT


@router.put(
    "/delete_user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "User successfully deleted."},
        status.HTTP_408_REQUEST_TIMEOUT: {"description": "Request timed out."},
    },
)
async def delete_user(
    user_id: UserId,
    response: Response,
    settings: Annotated[GeneralSettings, Depends(get_general_settings)],
    repo: Annotated[UserRepository, Depends(get_repository)],
):
    try:
        await asyncio.wait_for(repo.delete_user(user_id), settings.request_timeout_in_s)
    except asyncio.TimeoutError:
        logger.error(f"Timeout while calling delete_user(id={user_id}).")
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
