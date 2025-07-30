from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from userdb import db


@pytest.mark.asyncio
async def test_lifespan_creates_tables_when_missing(monkeypatch):
    """Test that lifespan creates tables if they do not exist."""
    mock_engine = MagicMock()
    mock_conn_ctx = AsyncMock()
    mock_conn = MagicMock()
    mock_run_sync = AsyncMock()
    mock_conn_ctx.__aenter__.return_value = mock_conn
    mock_conn.run_sync = mock_run_sync
    mock_engine.begin.return_value = mock_conn_ctx

    monkeypatch.setattr(db, "create_async_engine", lambda *a, **kw: mock_engine)
    monkeypatch.setattr(db, "async_sessionmaker", lambda *a, **kw: MagicMock())
    monkeypatch.setattr(
        db, "Settings", lambda: MagicMock(DATABASE_URL="sqlite+aiosqlite:///test.db")
    )

    # Patch session.execute to return a mock result with scalars().first() async
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first = AsyncMock(return_value=None)
    mock_result.scalars.return_value = mock_scalars
    monkeypatch.setattr(db, "add_admin_user", AsyncMock())
    monkeypatch.setattr(db, "AsyncSession", MagicMock())

    # Simulate tables do not exist
    def check_tables_exist(sync_conn):
        return False

    mock_run_sync.side_effect = [False, None]  # First for check, second for create_all

    with patch.object(db.Base.metadata, "create_all") as mock_create_all, patch.object(
        db, "logger"
    ) as mock_logger:
        async with db.lifespan():
            pass
        # Should call create_all
        assert mock_run_sync.call_count == 2
        mock_logger.info.assert_any_call("Creating missing tables in the database.")
        mock_create_all.assert_not_called()  # create_all is called via run_sync, not directly


@pytest.mark.asyncio
async def test_lifespan_skips_creation_when_tables_exist(monkeypatch):
    """Test that lifespan skips table creation if all tables exist."""
    mock_engine = MagicMock()
    mock_conn_ctx = AsyncMock()
    mock_conn = MagicMock()
    mock_run_sync = AsyncMock()
    mock_conn_ctx.__aenter__.return_value = mock_conn
    mock_conn.run_sync = mock_run_sync
    mock_engine.begin.return_value = mock_conn_ctx

    monkeypatch.setattr(db, "create_async_engine", lambda *a, **kw: mock_engine)
    monkeypatch.setattr(db, "async_sessionmaker", lambda *a, **kw: MagicMock())
    monkeypatch.setattr(
        db, "Settings", lambda: MagicMock(DATABASE_URL="sqlite+aiosqlite:///test.db")
    )

    # Patch session.execute to return a mock result with scalars().first() async
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first = AsyncMock(return_value=None)
    mock_result.scalars.return_value = mock_scalars
    monkeypatch.setattr(db, "add_admin_user", AsyncMock())
    monkeypatch.setattr(db, "AsyncSession", MagicMock())
    # Simulate tables exist
    mock_run_sync.side_effect = [True]

    with patch.object(db, "logger") as mock_logger:
        async with db.lifespan():
            pass
        # Should only check tables, not create
        assert mock_run_sync.call_count == 1
        mock_logger.info.assert_any_call("All tables already exist. Skipping creation.")


@pytest.mark.asyncio
async def test_lifespan_sets_dbstate(monkeypatch):
    """Test that lifespan sets DBState.engine and DBState.async_session_maker."""
    mock_engine = MagicMock()
    mock_conn_ctx = AsyncMock()
    mock_conn = MagicMock()
    mock_run_sync = AsyncMock()
    mock_conn_ctx.__aenter__.return_value = mock_conn
    mock_conn.run_sync = mock_run_sync
    mock_engine.begin.return_value = mock_conn_ctx

    # Use a MagicMock that is callable and can be used as a context manager
    class DummySessionMaker:
        def __call__(self, *a, **kw):
            class DummyContext:
                async def __aenter__(self):
                    return AsyncMock()

                async def __aexit__(self, exc_type, exc, tb):
                    pass

            return DummyContext()

    monkeypatch.setattr(db, "create_async_engine", lambda *a, **kw: mock_engine)
    monkeypatch.setattr(db, "async_sessionmaker", lambda *a, **kw: DummySessionMaker())
    monkeypatch.setattr(
        db,
        "Settings",
        lambda: MagicMock(
            DATABASE_URL="sqlite+aiosqlite:///test.db",
            ADMIN_EMAIL="admin@example.com",
            ADMIN_PASSWORD="changeme",
            ADMIN_FULL_NAME="Admin",
        ),
    )
    # Patch session.execute to return a mock result with scalars().first() async
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.first = AsyncMock(return_value=None)
    mock_result.scalars.return_value = mock_scalars
    monkeypatch.setattr(db, "add_admin_user", AsyncMock())
    monkeypatch.setattr(db, "AsyncSession", MagicMock())
    mock_run_sync.side_effect = [True]

    async with db.lifespan():
        pass
    assert db.DBState.engine is mock_engine
    assert isinstance(db.DBState.async_session_maker, DummySessionMaker)


@pytest.mark.asyncio
async def test_get_async_session_yields_session(monkeypatch):
    """Test get_async_session yields a session from the session maker."""

    class AsyncSessionContextManager:
        def __init__(self, session):
            self.session = session

        async def __aenter__(self):
            return self.session

        async def __aexit__(self, exc_type, exc, tb):
            pass

    mock_session = AsyncMock()
    db.DBState.async_session_maker = lambda: AsyncSessionContextManager(mock_session)
    gen = db.get_async_session()
    session = await gen.__anext__()
    assert session is mock_session


@pytest.mark.asyncio
async def test_get_async_session_raises_if_not_initialized(monkeypatch):
    """Test get_async_session raises if async_session_maker is None."""
    db.DBState.async_session_maker = None
    gen = db.get_async_session()
    with pytest.raises(RuntimeError, match="Database not initialized"):
        await gen.__anext__()


@pytest.mark.asyncio
async def test_get_user_db_yields_user_db(monkeypatch):
    """Test get_user_db yields a SQLAlchemyUserDatabase instance."""
    mock_session = MagicMock()
    with patch("userdb.db.SQLAlchemyUserDatabase", autospec=True) as mock_db:
        gen = db.get_user_db(mock_session)
        user_db = await gen.__anext__()
        mock_db.assert_called_once_with(mock_session, db.User)
        assert user_db == mock_db.return_value


def test_lifespan_check_tables_exist_integration(monkeypatch):
    """Integration test to cover check_tables_exist logic in lifespan."""
    import asyncio

    # Use a real in-memory SQLite database
    test_db_url = "sqlite+aiosqlite:///:memory:"
    monkeypatch.setattr(
        db,
        "Settings",
        lambda: type(
            "S",
            (),
            {
                "DATABASE_URL": test_db_url,
                "ADMIN_EMAIL": "admin@example.com",
                "ADMIN_PASSWORD": "changeme",
                "ADMIN_FULL_NAME": "Admin",
            },
        )(),
    )
    # Remove engine/sessionmaker mocks so real code runs
    db.DBState.engine = None
    db.DBState.async_session_maker = None

    # Patch add_admin_user to avoid TypeError in integration
    async def dummy_add_admin_user(session):
        pass

    monkeypatch.setattr(db, "add_admin_user", dummy_add_admin_user)

    async def run_lifespan_twice():
        with patch.object(db, "logger"):
            # First run: tables do not exist, so they will be created
            async with db.lifespan():
                pass
            # Second run: tables exist, so creation is skipped
            async with db.lifespan():
                pass

    asyncio.run(run_lifespan_twice())


@pytest.mark.asyncio
async def test_add_admin_user_skips_if_exists(monkeypatch):
    """Test add_admin_user returns early if an admin user already exists."""
    import uuid

    from sqlalchemy.ext.asyncio import AsyncSession  # For spec

    from userdb.models import User

    # 1. session is an AsyncMock
    session = AsyncMock(spec=AsyncSession)

    # 2. session.execute is an AsyncMock method.
    #    Its return_value is what `result` will be in `add_admin_user`
    mock_execute_yielded_result = MagicMock()
    session.execute = AsyncMock(return_value=mock_execute_yielded_result)

    # 3. mock_execute_yielded_result must have a .scalars() method (which is callable)
    mock_scalars_method_result = MagicMock()
    mock_execute_yielded_result.scalars.return_value = mock_scalars_method_result

    # 4. mock_scalars_method_result must have a .first() method (which is callable)
    existing_admin = User(
        id=uuid.uuid4(),
        email="admin@example.com",
        hashed_password="x",
        is_superuser=True,
        is_active=True,
        is_verified=True,
    )
    mock_scalars_method_result.first.return_value = existing_admin

    session.add = MagicMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    await db.add_admin_user(session)

    session.execute.assert_awaited_once()
    mock_execute_yielded_result.scalars.assert_called_once()
    mock_scalars_method_result.first.assert_called_once()

    session.add.assert_not_called()
    session.flush.assert_not_called()
    session.commit.assert_not_called()
    session.refresh.assert_not_called()


@pytest.mark.asyncio
async def test_lifespan_calls_add_admin_user(monkeypatch):
    """Test that lifespan calls add_admin_user during startup."""
    mock_engine = MagicMock()
    mock_conn_ctx = AsyncMock()
    mock_conn = MagicMock()
    mock_run_sync = AsyncMock()
    mock_conn_ctx.__aenter__.return_value = mock_conn
    mock_conn.run_sync = mock_run_sync
    mock_engine.begin.return_value = mock_conn_ctx

    monkeypatch.setattr(db, "create_async_engine", lambda *a, **kw: mock_engine)
    monkeypatch.setattr(db, "async_sessionmaker", lambda *a, **kw: MagicMock())
    monkeypatch.setattr(
        db, "Settings", lambda: MagicMock(DATABASE_URL="sqlite+aiosqlite:///test.db")
    )
    mock_run_sync.side_effect = [True]

    called = {}

    async def fake_add_admin_user(session):
        called["called"] = True

    monkeypatch.setattr(db, "add_admin_user", fake_add_admin_user)

    async with db.lifespan():
        pass
    assert called.get("called") is True
