from datetime import UTC, datetime

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from userdb.db import get_async_session
from userdb.models import APIKey, User
from userdb.userdb_utils import hash_api_key

api_key_header = APIKeyHeader(name="X-API-Key")


async def get_api_key_user(
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """FastAPI dependency that validates API key and returns associated user.

    Args:
        api_key: The API key from the X-API-Key header
        session: Database session

    Returns:
        User: The user associated with the API key

    Raises:
        HTTPException: 401 if API key is invalid
    """
    # Hash the incoming API key
    key_hash = hash_api_key(api_key)

    # Look up the API key record
    result = await session.execute(
        select(APIKey).where(APIKey.key_hash == key_hash, APIKey.status == "active")
    )
    api_key_record = result.scalar_one_or_none()

    if not api_key_record:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Get the associated user
    result = await session.execute(
        select(User).where(User.id == api_key_record.user_id)
    )
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    # Update last_used_at
    api_key_record.last_used_at = datetime.now(UTC)
    await session.commit()

    return user
