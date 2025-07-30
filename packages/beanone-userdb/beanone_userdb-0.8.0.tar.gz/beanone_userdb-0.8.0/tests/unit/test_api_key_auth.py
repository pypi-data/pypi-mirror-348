from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from userdb.api_key_auth import get_api_key_user
from userdb.models import APIKey, User


@pytest.fixture
def mock_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_user():
    return User(
        id="user-123",
        email="test@example.com",
        hashed_password="hashed",
        is_active=True,
        is_verified=True,
        is_superuser=False,
    )


@pytest.fixture
def mock_api_key(mock_user):
    return APIKey(
        id="key-123",
        user_id=mock_user.id,
        key_hash="hashed_key",
        service_id="test-service",
        name="Test Key",
        status="active",
        created_at=datetime.now(UTC),
    )


@pytest.mark.asyncio
async def test_get_api_key_user_success(mock_session, mock_user, mock_api_key):
    """Test successful API key authentication."""
    # Setup mock API key lookup
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_api_key
    mock_session.execute.return_value = mock_result

    # Setup mock user lookup
    mock_user_result = MagicMock()
    mock_user_result.scalar_one_or_none.return_value = mock_user
    mock_session.execute.side_effect = [mock_result, mock_user_result]

    # Test with a valid API key
    api_key = "valid_api_key"
    user = await get_api_key_user(api_key=api_key, session=mock_session)

    # Verify results
    assert user == mock_user
    assert mock_session.execute.call_count == 2
    mock_session.commit.assert_called_once()
    assert mock_api_key.last_used_at is not None


@pytest.mark.asyncio
async def test_get_api_key_user_invalid_key(mock_session):
    """Test authentication with invalid API key."""
    # Setup mock to return None for invalid key
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    # Test with an invalid API key
    api_key = "invalid_api_key"
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key_user(api_key=api_key, session=mock_session)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid API key"
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_get_api_key_user_inactive_user(mock_session, mock_api_key):
    """Test authentication with inactive user."""
    # Setup mock API key lookup
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_api_key
    mock_session.execute.return_value = mock_result

    # Setup mock user lookup to return None (inactive user)
    mock_user_result = MagicMock()
    mock_user_result.scalar_one_or_none.return_value = None
    mock_session.execute.side_effect = [mock_result, mock_user_result]

    # Test with valid API key but inactive user
    api_key = "valid_api_key"
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key_user(api_key=api_key, session=mock_session)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "User not found or inactive"
    assert mock_session.execute.call_count == 2
    mock_session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_get_api_key_user_inactive_key(mock_session, mock_user):
    """Test authentication with inactive API key."""
    # Setup mock to return None for inactive key
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    # Test with inactive API key
    api_key = "valid_api_key"
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key_user(api_key=api_key, session=mock_session)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid API key"
    mock_session.execute.assert_called_once()
    mock_session.commit.assert_not_called()
