from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from userdb.models import APIKey
from userdb.userdb_utils import create_api_key_record


async def create_api_key(
    user_id: str,
    service_id: str,
    session: AsyncSession,
    name: str | None = None,
    expires_at: datetime | None = None,
) -> dict:
    """Create a new API key for the given user.

    Args:
        user_id (str): The user's stringified UUID.
        service_id (str): The service identifier.
        session (AsyncSession): SQLAlchemy async session.
        name (Optional[str]): Optional name for the key.
        expires_at (Optional[datetime]): Optional expiration.

    Returns:
        dict: API key info including plaintext key.
    """
    plaintext_key, api_key_obj = create_api_key_record(
        user_id=user_id,
        service_id=service_id,
        name=name,
        expires_at=expires_at,
    )
    session.add(api_key_obj)
    await session.commit()
    await session.refresh(api_key_obj)
    return {
        "id": api_key_obj.id,
        "name": api_key_obj.name,
        "service_id": api_key_obj.service_id,
        "status": api_key_obj.status,
        "created_at": api_key_obj.created_at,
        "expires_at": api_key_obj.expires_at,
        "last_used_at": api_key_obj.last_used_at,
        "plaintext_key": plaintext_key,
    }


async def list_api_keys(
    user_id: str,
    session: AsyncSession,
) -> list[dict]:
    """List all API keys for the given user.

    Args:
        user_id (str): The user's stringified UUID.
        session (AsyncSession): SQLAlchemy async session.

    Returns:
        List[dict]: List of API key info dicts.
    """
    result = await session.execute(select(APIKey).where(APIKey.user_id == user_id))
    keys = result.scalars().all()
    return [
        {
            "id": row.id,
            "name": row.name,
            "service_id": row.service_id,
            "status": row.status,
            "created_at": row.created_at,
            "expires_at": row.expires_at,
            "last_used_at": row.last_used_at,
        }
        for row in keys
    ]


async def delete_api_key(
    key_id: str,
    user_id: str,
    session: AsyncSession,
) -> bool:
    """Delete (revoke) an API key by ID for the given user.

    Args:
        key_id (str): The API key ID.
        user_id (str): The user's stringified UUID.
        session (AsyncSession): SQLAlchemy async session.

    Returns:
        bool: True if deleted, False if not found.
    """
    result = await session.execute(
        select(APIKey).where(APIKey.id == key_id, APIKey.user_id == user_id)
    )
    row = result.first()
    if not row:
        return False
    await session.execute(
        APIKey.__table__.delete().where(APIKey.id == key_id, APIKey.user_id == user_id)
    )
    await session.commit()
    return True
