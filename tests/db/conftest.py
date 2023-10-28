import pytest_asyncio

from event_handler.db.sqlite import Sqlite


@pytest_asyncio.fixture
async def sqlite() -> Sqlite:
    # SetUp
    db = Sqlite(path=":memory:")
    await db.connect()
    # Entry
    yield db
    # TearDown
    await db.disconnect()
