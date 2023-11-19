import pytest

from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


@pytest.fixture(autouse=True)
async def user_service(db):
    _db = await db
    user_repo = UserRepository(_db)
    user_service = UserService(user_repository=user_repo)
    return user_service


@pytest.mark.asyncio
async def test_user_service(user_service):
    us = await user_service
    assert isinstance(us, UserService)


@pytest.mark.asyncio
async def test_user_service_create_user(user_service):
    us = await user_service
    user = await us.create_user(name="test")
    assert user is not None
    assert "id" in user.model_dump()
    assert user.name == "test"


@pytest.mark.asyncio
async def test_user_service_get_user(user_service):
    us = await user_service
    created_user = await us.create_user(name="test")
    user = await us.get_user(_id=created_user.id)
    assert user is not None
    assert user.id == created_user.id


@pytest.mark.asyncio
async def test_user_service_get_user_not_found(user_service):
    us = await user_service
    user = await us.get_user(_id="6559dd0631889d2c71931f07")
    assert user is None


@pytest.mark.asyncio
async def test_user_service_get_user_invalid_id(user_service):
    us = await user_service
    with pytest.raises(ValueError) as exif:
        await us.get_user(_id="invalid_id")
    assert "Invalid id" in str(exif.value)


@pytest.mark.asyncio
async def test_user_service_get_all_users(user_service):
    us = await user_service
    user = await us.create_user(name="test")
    users = await us.get_all_users()
    assert users is not None
    assert len(users) == 1
    assert users[0].id == user.id


@pytest.mark.asyncio
async def test_user_service_get_all_users_empty(user_service):
    us = await user_service
    users = await us.get_all_users()
    assert users is not None
    assert len(users) == 0


@pytest.mark.asyncio
async def test_user_service_get_all_users_more_than_one(user_service):
    us = await user_service
    await us.create_user(name="test")
    await us.create_user(name="test2")
    users = await us.get_all_users()
    assert users is not None
    assert len(users) == 2
    assert users[0].name == "test"
    assert users[1].name == "test2"


@pytest.mark.asyncio
async def test_user_service_update_user(user_service):
    us = await user_service
    user = await us.create_user(name="test")
    await us.update_user(_id=user.id, name="test2")
    user = await us.get_user(_id=user.id)
    assert user is not None
    assert user.name == "test2"


@pytest.mark.asyncio
async def test_user_service_update_user_not_found(user_service):
    us = await user_service
    user = await us.update_user(_id="6559dd0631889d2c71931f07", name="test2")
    assert user is None


@pytest.mark.asyncio
async def test_user_service_update_user_invalid_id(user_service):
    us = await user_service
    with pytest.raises(ValueError) as exif:
        await us.update_user(_id="invalid_id", name="test2")

    assert "Invalid id" in str(exif.value)


@pytest.mark.asyncio
async def test_user_service_delete_user(user_service):
    us = await user_service
    user = await us.create_user(name="test")
    await us.delete_user(_id=user.id)
    user = await us.get_user(_id=user.id)
    assert user is None


@pytest.mark.asyncio
async def test_user_service_delete_user_not_found(user_service):
    us = await user_service
    user = await us.delete_user(_id="6559dd0631889d2c71931f07")
    assert user is None


@pytest.mark.asyncio
async def test_user_service_delete_user_invalid_id(user_service):
    us = await user_service
    with pytest.raises(ValueError) as exif:
        await us.delete_user(_id="invalid_id")

    assert "Invalid id" in str(exif.value)
