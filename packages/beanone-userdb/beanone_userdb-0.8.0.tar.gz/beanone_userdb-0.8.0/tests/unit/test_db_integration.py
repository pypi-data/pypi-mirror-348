import uuid

import pytest

from userdb import db, models


@pytest.mark.asyncio
async def test_dbpy_crud_with_lifespan_and_get_async_session(monkeypatch):
    """Test CRUD operations using db.py's session and lifespan logic with SQLite."""
    # Mock Settings to use in-memory SQLite
    monkeypatch.setattr(
        db,
        "Settings",
        lambda: type(
            "S",
            (),
            {
                "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
                "ADMIN_EMAIL": "admin@example.com",
                "ADMIN_PASSWORD": "changeme",
                "ADMIN_FULL_NAME": "Admin",
            },
        )(),
    )

    # Reset DBState
    db.DBState.engine = None
    db.DBState.async_session_maker = None

    async with db.lifespan():
        # Use get_async_session to get a session
        gen = db.get_async_session()
        session = await gen.__anext__()

        # Create a user
        user_id = uuid.uuid4()
        user = models.User(
            id=user_id,
            email="test@example.com",
            hashed_password="hashed",
            full_name="Test User",
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
        session.add(user)
        await session.commit()

        # Create an APIKey for the user
        apikey = models.APIKey(
            user_id=str(user_id),
            key_hash="hash123",
            service_id="service1",
            name="Key 1",
        )
        session.add(apikey)
        await session.commit()

        # Query and assert
        user_db = await session.get(models.User, user_id)
        assert user_db is not None
        result = await session.execute(
            models.APIKey.__table__.select().where(
                models.APIKey.user_id == str(user_id)
            )
        )
        apikeys = result.fetchall()
        assert len(apikeys) == 1
        assert apikeys[0].name == "Key 1"


@pytest.mark.asyncio
async def test_apikey_cascade_delete_with_user(monkeypatch):
    """Test that deleting a User cascades and deletes their APIKeys."""
    # Mock Settings to use in-memory SQLite
    monkeypatch.setattr(
        db,
        "Settings",
        lambda: type(
            "S",
            (),
            {
                "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
                "ADMIN_EMAIL": "admin@example.com",
                "ADMIN_PASSWORD": "changeme",
                "ADMIN_FULL_NAME": "Admin",
            },
        )(),
    )

    # Reset DBState
    db.DBState.engine = None
    db.DBState.async_session_maker = None

    async with db.lifespan():
        gen = db.get_async_session()
        session = await gen.__anext__()

        # Create a user
        user_id = uuid.uuid4()
        user = models.User(
            id=user_id,
            email="test2@example.com",
            hashed_password="hashed",
            full_name="Test User 2",
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
        session.add(user)
        await session.commit()

        # Create an APIKey for the user
        apikey = models.APIKey(
            user_id=str(user_id),
            key_hash="hash456",
            service_id="service2",
            name="Key 2",
        )
        session.add(apikey)
        await session.commit()

        # Confirm APIKey exists
        result = await session.execute(
            models.APIKey.__table__.select().where(
                models.APIKey.user_id == str(user_id)
            )
        )
        apikeys = result.fetchall()
        assert len(apikeys) == 1

        # Delete the user
        await session.delete(user)
        await session.commit()

        # APIKey should be deleted
        result = await session.execute(
            models.APIKey.__table__.select().where(
                models.APIKey.user_id == str(user_id)
            )
        )
        apikeys_after = result.fetchall()
        assert len(apikeys_after) == 0
