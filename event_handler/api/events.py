import asyncio

from fastapi import APIRouter, Depends, Response, status
from typing_extensions import Annotated

from event_handler.api.config import GeneralSettings, get_database, get_general_settings
from event_handler.db.interface import Database
from event_handler.logger import logger
from event_handler.models.event import Event, EventId, EventKey, EventWithId
from event_handler.models.user import UserId
from event_handler.repositories.event_repo import EventRepository

router = APIRouter(prefix="/api/v1.0/events", tags=["events"], responses={404: {"description": "Not found"}})


async def get_repository(database: Annotated[Database, Depends(get_database)]) -> EventRepository:
    if not database.is_connected():
        await database.connect()
    repo = EventRepository(db=database)
    await repo.create_repository()
    return repo


@router.put(
    "/create_event",
    status_code=status.HTTP_200_OK,
    response_model=EventKey,
    responses={
        status.HTTP_200_OK: {"description": "Event successfully created"},
        status.HTTP_408_REQUEST_TIMEOUT: {"description": "Request timed out."},
    },
)
async def create_event(
    event: Event,
    response: Response,
    settings: Annotated[GeneralSettings, Depends(get_general_settings)],
    repo: Annotated[EventRepository, Depends(get_repository)],
):
    try:
        id = await asyncio.wait_for(repo.create_event(event), settings.request_timeout_in_s)
        logger.info(f"Created new event at id={id}")
        return {"id": str(id)}
    except asyncio.TimeoutError:
        logger.error("Timeout while calling create_event().")
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT


@router.put(
    "/get_event/{event_id}",
    status_code=status.HTTP_200_OK,
    response_model=EventWithId | None,
    responses={
        status.HTTP_200_OK: {"description": "Event successfully created."},
        status.HTTP_404_NOT_FOUND: {"description": "Event not found."},
        status.HTTP_408_REQUEST_TIMEOUT: {"description": "Request timed out."},
    },
)
async def get_event(
    event_id: EventId,
    response: Response,
    settings: Annotated[GeneralSettings, Depends(get_general_settings)],
    repo: Annotated[EventRepository, Depends(get_repository)],
):
    try:
        event = await asyncio.wait_for(repo.get_event(event_id), settings.request_timeout_in_s)
        if event is not None:
            return event.__dict__
        else:
            logger.error(f"Invalid event id={event_id}.")
            response.status_code = status.HTTP_404_NOT_FOUND
    except asyncio.TimeoutError:
        logger.error(f"Timeout while calling get_event(id={event_id}).")
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT


@router.put(
    "/add_attendees_to_event/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Event successfully updated."},
        status.HTTP_404_NOT_FOUND: {"description": "Event not found."},
        status.HTTP_408_REQUEST_TIMEOUT: {"description": "Request timed out."},
    },
)
async def add_attendees_to_event(
    event_id: EventId,
    user_ids: list[UserId],
    response: Response,
    settings: Annotated[GeneralSettings, Depends(get_general_settings)],
    repo: Annotated[EventRepository, Depends(get_repository)],
):
    try:
        is_succesful = await asyncio.wait_for(
            repo.add_attendees_to_event(event_id, user_ids), settings.request_timeout_in_s
        )
        if not is_succesful:
            logger.error(f"Invalid event id={event_id}.")
            response.status_code = status.HTTP_404_NOT_FOUND
    except asyncio.TimeoutError:
        logger.error(f"Timeout while calling add_attendees_to_event(id={event_id}).")
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT


@router.put(
    "/delete_event/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Event successfully deleted."},
        status.HTTP_408_REQUEST_TIMEOUT: {"description": "Request timed out."},
    },
)
async def delete_event(
    event_id: EventId,
    response: Response,
    settings: Annotated[GeneralSettings, Depends(get_general_settings)],
    repo: Annotated[EventRepository, Depends(get_repository)],
):
    try:
        await asyncio.wait_for(repo.delete_event(event_id), settings.request_timeout_in_s)
    except asyncio.TimeoutError:
        logger.error(f"Timeout while calling add_attendees_to_event(id={event_id}).")
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
