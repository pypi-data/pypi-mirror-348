import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.password import PasswordHelper
from sqlalchemy import event, inspect, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import Settings
from .models import Base, User


class DBState:
    engine = None
    async_session_maker = None


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan():
    """Lifespan context for FastAPI app, initializes DB if needed."""
    settings = Settings()
    DBState.engine = create_async_engine(settings.DATABASE_URL, echo=True)
    DBState.async_session_maker = async_sessionmaker(
        DBState.engine, expire_on_commit=False
    )

    # Enable SQLite foreign key support if using SQLite
    if DBState.engine.url.get_backend_name() == "sqlite":

        @event.listens_for(DBState.engine.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()  # pragma: no cover

    async with DBState.engine.begin() as conn:
        # Check if all tables exist
        def check_tables_exist(sync_conn):
            inspector = inspect(sync_conn)
            existing_tables = inspector.get_table_names()
            expected_tables = Base.metadata.tables.keys()
            return all(table in existing_tables for table in expected_tables)

        tables_exist = await conn.run_sync(check_tables_exist)
        if not tables_exist:
            logger.info("Creating missing tables in the database.")
            await conn.run_sync(Base.metadata.create_all)
        else:
            logger.info("All tables already exist. Skipping creation.")

    async with DBState.async_session_maker() as session:
        await add_admin_user(session)

    yield


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    if DBState.async_session_maker is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with DBState.async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def add_admin_user(session: AsyncSession) -> None:
    """
    Add an admin user to the database if it doesn't exist.

    Args:
        session (AsyncSession): The database session.

    Returns:
        None
    """
    result = await session.execute(select(User).where(User.is_superuser.is_(True)))
    admin = result.scalars().first()
    if admin:
        return

    settings = Settings()
    password_helper = PasswordHelper()
    admin = User(
        email=settings.ADMIN_EMAIL,
        hashed_password=password_helper.hash(settings.ADMIN_PASSWORD),
        is_superuser=True,
        is_active=True,
        is_verified=True,
        full_name=settings.ADMIN_FULL_NAME,
    )
    session.add(admin)
    await session.flush()
    await session.commit()
    await session.refresh(admin)
