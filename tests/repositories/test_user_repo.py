import pytest

from event_handler.db.interface import Database
from event_handler.models.user import User
from event_handler.repositories.user_repo import UserRepository


@pytest.mark.asyncio
async def test_when_user_repository_is_created_then_no_error_is_thrown(database: Database):
    """Test that no error is thrown when creating a repository."""
    # Arrange
    repo = UserRepository(db=database)

    # Act & Assert
    try:
        await repo.create_repository()

    except Exception:
        assert False, "Could not create repository."


@pytest.mark.asyncio
async def test_when_user_repository_is_created_and_users_inserted_then_no_error_is_thrown(database: Database):
    """Test that no error is thrown when creating a repository and inserting users."""
    # Arrange
    repo = UserRepository(db=database)
    user = User(first_name="Mr", last_name="Bond", email="MrBond@email.de")

    # Act & Assert
    try:
        await repo.create_repository()
        _ = await repo.create_user(user=user)

    except Exception:
        assert False, "Could not create repository."


@pytest.mark.asyncio
async def test_when_user_repository_is_created_and_users_inserted_then_keys_are_incremented(database: Database):
    """Test that the primary keys of the users are incremented when inserting users."""
    # Arrange
    repo = UserRepository(db=database)
    user = User(first_name="Mr", last_name="Bond", email="MrBond@email.de")
    number_of_users = 5
    await repo.create_repository()

    # Act & Assert
    for i in range(1, number_of_users):
        new_id = await repo.create_user(user=user)
        assert new_id == i


@pytest.mark.asyncio
async def test_when_user_repository_is_created_and_users_inserted_then_users_can_bet_fetched_by_id(
    database: Database,
):
    """Test that the users can be fetched by their id after inserting them."""
    # Arrange
    repo = UserRepository(db=database)
    user = User(first_name="Son", last_name="Goku", email="SonGoku@email.com")
    number_of_users = 5
    await repo.create_repository()

    # Act
    for _ in range(1, number_of_users):
        await repo.create_user(user=user)

    # Assert
    for i in range(1, number_of_users):
        user = await repo.get_user(id=i)
        assert user.id == i


@pytest.mark.asyncio
async def test_when_user_repository_is_created_and_users_deleted_then_user_is_not_in_database(
    database: Database,
):
    """Test that the users are not in the database after deleting them."""
    # Arrange
    repo = UserRepository(db=database)
    user = User(first_name="Son", last_name="Goku", email="SonGoku@email.com")
    number_of_users = 5
    await repo.create_repository()

    # Act
    for _ in range(1, number_of_users):
        await repo.create_user(user=user)

    # Assert
    for i in range(1, number_of_users):
        user = await repo.get_user(id=i)
        assert user.id == i

    # Act
    for i in range(1, number_of_users):
        await repo.delete_user(id=i)

    # Assert
    for i in range(1, number_of_users):
        user = await repo.get_user(id=i)
        assert user is None
