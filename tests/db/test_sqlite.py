import pytest

from event_handler.db.sqlite import Sqlite


@pytest.mark.asyncio
async def test_when_database_is_connected_table_created_then_db_is_connected(sqlite: Sqlite):
    # Act & Assert
    assert sqlite.is_connected()


@pytest.mark.asyncio
async def test_when_database_is_connected_table_created_then_no_error_is_thrown(sqlite: Sqlite):
    # Arrange
    table_name = "test_table"
    schema = "id text PRIMARY KEY, value integer"

    # Act & Assert
    try:
        await sqlite.create_table_if_not_exists(table_name=table_name, schema=schema)
    except Exception:
        assert False, "Could not create table."


@pytest.mark.asyncio
async def test_when_database_is_connected_and_table_created_then_values_are_empty(sqlite: Sqlite):
    # Arrange
    table_name = "test_table"
    schema = "id text PRIMARY KEY, value integer"

    # Act
    await sqlite.create_table_if_not_exists(table_name=table_name, schema=schema)
    values = await sqlite.select_all_data(table_name=table_name)

    # Assert
    assert len(values) == 0


@pytest.mark.asyncio
async def test_when_database_is_connected_and_values_inserted_then_values_are_valid(sqlite: Sqlite):
    # Arrange
    table_name = "test_table"
    schema = "id text PRIMARY KEY, value integer"
    data = {"id": "123ABC", "value": 42}

    # Act
    await sqlite.create_table_if_not_exists(table_name=table_name, schema=schema)
    await sqlite.insert_data(table_name=table_name, data=data)
    values = await sqlite.select_all_data(table_name=table_name)

    # Assert
    assert len(values) == 1
    assert values[0][0] == data["id"]
    assert values[0][1] == data["value"]


@pytest.mark.asyncio
async def test_when_database_is_connected_and_multiple_values_inserted_then_values_are_valid(sqlite: Sqlite):
    # Arrange
    table_name = "test_table"
    schema = "id text PRIMARY KEY, value integer"
    data = [{"id": "123ABC", "value": 42}, {"id": "43123A", "value": 1337}]
    await sqlite.create_table_if_not_exists(table_name=table_name, schema=schema)

    # Act
    for i in range(0, len(data)):
        await sqlite.insert_data(table_name=table_name, data=data[i])
    values = await sqlite.select_all_data(table_name=table_name)

    # Assert
    assert len(values) == 2
    for i in range(0, len(data)):
        assert values[i][0] == data[i]["id"]
        assert values[i][1] == data[i]["value"]


@pytest.mark.asyncio
async def test_when_database_is_connected_and_multiple_values_inserted_then_values_can_be_fetched_by_key(
    sqlite: Sqlite,
):
    # Arrange
    table_name = "test_table"
    schema = "id text PRIMARY KEY, value integer"
    data = [{"id": "123ABC", "value": 42}, {"id": "43123A", "value": 1337}]
    await sqlite.create_table_if_not_exists(table_name=table_name, schema=schema)

    # Act
    for i in range(0, len(data)):
        await sqlite.insert_data(table_name=table_name, data=data[i])
    values = await sqlite.select_all_data_by_key_and_value(table_name=table_name, key="id", value=data[0]["id"])

    # Assert
    assert len(values) == 1
    assert values[0][0] == data[0]["id"]
    assert values[0][1] == data[0]["value"]


@pytest.mark.asyncio
async def test_when_database_is_connected_and_values_inserted_and_updated_then_values_are_valid(sqlite: Sqlite):
    # Arrange
    table_name = "test_table"
    schema = "id text PRIMARY KEY, value integer"
    data = [{"id": "123ABC", "value": 42}, {"id": "43123A", "value": 1337}]
    new_data = {"id": "123ABC", "value": 9000}
    await sqlite.create_table_if_not_exists(table_name=table_name, schema=schema)

    # Act
    for i in range(0, len(data)):
        await sqlite.insert_data(table_name=table_name, data=data[i])
    await sqlite.replace_data(table_name=table_name, data=new_data)
    values = await sqlite.select_all_data_by_key_and_value(table_name=table_name, key="id", value=data[0]["id"])

    # Assert
    assert len(values) == 1
    assert values[0][0] == new_data["id"]
    assert values[0][1] == new_data["value"]


@pytest.mark.asyncio
async def test_when_database_is_connected_and_values_and_then_deleted_then_values_are_valid(sqlite: Sqlite):
    # Arrange
    table_name = "test_table"
    schema = "id text PRIMARY KEY, value integer"
    data = {"id": "123ABC", "value": 9000}
    await sqlite.create_table_if_not_exists(table_name=table_name, schema=schema)

    # Act
    await sqlite.insert_data(table_name=table_name, data=data)
    values = await sqlite.select_all_data(table_name=table_name)

    # Assert
    assert len(values) == 1

    # Act
    await sqlite.delete_data_by_key_and_value(table_name=table_name, key="id", value=data["id"])
    values = await sqlite.select_all_data(table_name=table_name)

    # Assert
    assert len(values) == 0
