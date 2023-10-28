from event_handler.db.interface import Database
from event_handler.models.event import Event, EventId, EventWithId
from event_handler.models.user import UserId

Schema = str
IsSuccessful = bool


class EventRepository:
    def __init__(self, db: Database):
        """Initializes the EventRepository with a Database object.

        Args:
            db (Database): The database object that handles the connection and queries.
        """
        self._db = db

    @property
    def _table_name(self) -> str:
        """Returns the name of the table that stores the Events.

        Returns:
            str: The name of the table.
        """
        return "Events"

    @property
    def _schema(self) -> Schema:
        """Returns the schema of the table that stores the Events.

        Returns:
            Schema: The schema of the table.
        """
        return (
            "id integer NOT NULL PRIMARY KEY AUTOINCREMENT,"
            "name TEXT NOT NULL,"
            "time DATETIME NOT NULL,"
            "location TEXT NOT NULL,"
            "description TEXT NOT NULL,"
            "attendees TEXT"  # Use TEXT to store a list of user ids as a comma-separated string
        )

    async def create_repository(self):
        """Creates the table for events if it does not exist in the database."""
        await self._db.create_table_if_not_exists(table_name=self._table_name, schema=self._schema)

    async def create_event(self, event: Event) -> EventId:
        """Inserts a new event into the database and returns its id.

        Args:
            event (Event): The event object to be inserted.

        Returns:
            EventId: The id of the inserted event.
        """
        id = await self._db.insert_data(
            table_name=self._table_name,
            data={
                "name": event.name,
                "time": event.time,
                "location": event.location,
                "description": event.description,
                "attendees": ",".join(str(s) for s in event.attendees) if event.attendees is not None else "",
            },
        )
        return id[0]

    async def add_attendees_to_event(self, id: EventId, attendees: list[UserId] | UserId) -> IsSuccessful:
        """Adds one or more attendees to an existing event and returns its id.

        Args:
            id (EventId): The id of the event to be updated.
            attendees (list[UserId] | UserId): The user id or a list of user ids to be added as attendees.
        """
        if not isinstance(attendees, list):  # skip: coverage
            attendees = [attendees]

        event = await self.get_event(id=id)
        if event is None:  # skip: coverage
            return False

        await self._db.replace_data(
            table_name=self._table_name,
            data={
                "id": event.id,
                "name": event.name,
                "time": event.time,
                "location": event.location,
                "description": event.description,
                "attendees": ",".join(str(s) for s in attendees) if event.attendees is not None else "",
            },
        )
        return True

    async def get_event(self, id: EventId) -> EventWithId | None:
        """Retrieves a event from the database by its id.

        Args:
            id (EventId): The id of the event to be retrieved.

        Returns:
            Event | None: The event object if found, or None otherwise.
        """
        event = await self._db.select_all_data_by_key_and_value(table_name=self._table_name, key="id", value=id)
        if len(event) == 1:  # there is only one entry associated per id
            return EventWithId(
                id=event[0][0],
                name=event[0][1],
                time=event[0][2],
                location=event[0][3],
                description=event[0][4],
                attendees=set((id for id in event[0][5].split(","))) if event[0][5] != "" else set(),
            )

    async def delete_event(self, id: EventId):
        """Deletes a event from the database by its id.

        Args:
            id (EventId): The id of the event to be deleted.
        """
        await self._db.delete_data_by_key_and_value(table_name=self._table_name, key="id", value=id)
