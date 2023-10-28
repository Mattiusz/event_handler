from datetime import datetime

from pydantic import BaseModel

from event_handler.models.user import UserId

EventId = int


class Event(BaseModel):
    name: str
    time: datetime
    location: str
    description: str
    attendees: set[UserId] | None = None


class EventWithId(Event):
    id: EventId


class EventKey(BaseModel):
    id: EventId
