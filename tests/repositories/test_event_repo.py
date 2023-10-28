from datetime import datetime

import pytest

from event_handler.db.interface import Database
from event_handler.models.event import Event
from event_handler.repositories.event_repo import EventRepository


@pytest.mark.asyncio
async def test_when_event_repository_is_created_then_no_error_is_thrown(database: Database):
    """Test that no error is thrown when creating a repository."""
    # Arrange
    repo = EventRepository(db=database)

    # Act & Assert
    try:
        await repo.create_repository()

    except Exception:
        assert False, "Could not create repository."


@pytest.mark.asyncio
async def test_when_event_repository_is_created_and_events_inserted_then_no_error_is_thrown(database: Database):
    """Test that no error is thrown when creating a repository and inserting events."""
    # Arrange
    repo = EventRepository(db=database)
    event = Event(name="Partytime", time=datetime.now(), location="Reeperbahn", description="Dance and drink")

    # Act & Assert
    try:
        await repo.create_repository()
        _ = await repo.create_event(event=event)

    except Exception:
        assert False, "Could not create repository."


@pytest.mark.asyncio
async def test_when_event_repository_is_created_and_events_inserted_then_keys_are_incremented(database: Database):
    """Test that the primary keys of the events are incremented when inserting events."""
    # Arrange
    repo = EventRepository(db=database)
    event = Event(name="Partytime", time=datetime.now(), location="Reeperbahn", description="Dance and drink")
    number_of_events = 5
    await repo.create_repository()

    # Act & Assert
    for i in range(1, number_of_events):
        new_id = await repo.create_event(event=event)
        assert new_id == i


@pytest.mark.asyncio
async def test_when_event_repository_is_created_and_events_inserted_then_events_can_bet_fetched_by_id(
    database: Database,
):
    """Test that the events can be fetched by their id after inserting them."""
    # Arrange
    repo = EventRepository(db=database)
    event = Event(name="Chill", time=datetime.now(), location="At my house", description="")
    number_of_events = 5
    await repo.create_repository()

    # Act
    for _ in range(1, number_of_events):
        await repo.create_event(event=event)

    # Assert
    for i in range(1, number_of_events):
        event = await repo.get_event(id=i)
        assert event.id == i


@pytest.mark.asyncio
async def test_when_event_repository_is_created_and_events_deleted_then_event_is_not_in_database(
    database: Database,
):
    """Test that the events are not in the database after deleting them."""
    # Arrange
    repo = EventRepository(db=database)
    event = Event(name="Partytime", time=datetime.now(), location="Reeperbahn", description="Dance and drink")
    number_of_events = 5
    await repo.create_repository()

    # Act
    for _ in range(1, number_of_events):
        await repo.create_event(event=event)

    # Assert
    for i in range(1, number_of_events):
        event = await repo.get_event(id=i)
        assert event.id == i

    # Act
    for i in range(1, number_of_events):
        await repo.delete_event(id=i)

    # Assert
    for i in range(1, number_of_events):
        event = await repo.get_event(id=i)
        assert event is None


@pytest.mark.asyncio
async def test_when_events_are_inserted_and_attendees_are_added_then_event_is_valid(
    database: Database,
):
    # Arrange
    repo = EventRepository(db=database)
    event = Event(name="Partytime", time=datetime.now(), location="Reeperbahn", description="Dance and drink")
    attendees = [123, 42, 9000, 0]
    await repo.create_repository()

    # Act
    id = await repo.create_event(event=event)

    # Assert
    event = await repo.get_event(id=id)
    assert len(event.attendees) == 0

    # Act
    await repo.add_attendees_to_event(id=id, attendees=attendees)

    # Assert
    event = await repo.get_event(id=id)
    assert event.attendees == set(attendees)
