import hashlib
import logging
import secrets
import string
import uuid
from datetime import UTC, datetime, timedelta

from userdb.models import APIKey, APIKeyStatus

from .config import Settings

# Moved from userdb.auth
logger = logging.getLogger(__name__)


def create_jwt_for_user(
    user_id: uuid.UUID,
    email: str,
    expires_seconds: int = 3600,
    settings: Settings | None = None,
) -> str:
    """
    Create a JWT for a test user.

    Args:
        user_id (uuid.UUID): The user ID.
        email (str): The user's email.
        expires_seconds (int): Expiry in seconds.
        settings (Settings): The settings instance to use.

    Returns:
        str: Encoded JWT token.
    """
    import jwt

    from userdb.config import Settings

    settings = settings or Settings()
    now = datetime.now(UTC)
    exp = now + timedelta(seconds=expires_seconds or settings.JWT_EXPIRE_SECONDS)
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": exp,
        "iat": now,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def generate_api_key(length: int = 40) -> str:
    """Generate a secure random API key string.

    Args:
        length (int): Length of the API key.

    Returns:
        str: The generated API key (plaintext).
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def hash_api_key(api_key: str) -> str:
    """Hash an API key using SHA-256.

    Args:
        api_key (str): The plaintext API key.

    Returns:
        str: The hex-encoded SHA-256 hash of the API key.
    """
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def create_api_key_record(
    user_id: str,
    service_id: str,
    name: str | None = None,
    status: APIKeyStatus = APIKeyStatus.ACTIVE,
    expires_at: datetime | None = None,
    last_used_at: datetime | None = None,
    id: str | None = None,
    created_at: datetime | None = None,
    key_length: int = 40,
) -> tuple[str, APIKey]:
    """Generate a new API key, hash it, and create an APIKey record.

    Args:
        user_id (str): The user ID.
        service_id (str): The target service ID.
        name (str | None): Optional label for the key.
        status (APIKeyStatus): Key status (default ACTIVE).
        expires_at (datetime | None): Optional expiry.
        last_used_at (datetime | None): Optional last used.
        id (str | None): Optional key ID.
        created_at (datetime | None): Optional creation time.
        key_length (int): Length of the generated API key.

    Returns:
        tuple[str, APIKey]: (plaintext API key, APIKey record with hash)
    """
    api_key = generate_api_key(length=key_length)
    key_hash = hash_api_key(api_key)

    # Ensure created_at is naive UTC
    final_created_at: datetime | None
    if created_at:
        final_created_at = (
            created_at.replace(tzinfo=None) if created_at.tzinfo else created_at
        )
    else:
        final_created_at = datetime.now(UTC).replace(tzinfo=None)

    # Ensure expires_at is naive UTC if provided
    final_expires_at: datetime | None = None
    if expires_at:
        final_expires_at = (
            expires_at.replace(tzinfo=None) if expires_at.tzinfo else expires_at
        )

    # Ensure last_used_at is naive UTC if provided
    final_last_used_at: datetime | None = None
    if last_used_at:
        final_last_used_at = (
            last_used_at.replace(tzinfo=None) if last_used_at.tzinfo else last_used_at
        )

    record = APIKey(
        user_id=user_id,
        key_hash=key_hash,
        service_id=service_id,
        name=name,
        status=status,
        expires_at=final_expires_at,
        last_used_at=final_last_used_at,
        id=id,
        created_at=final_created_at,
    )
    return api_key, record


async def default_userdb_email_sender(*, to_email: str, token: str, path: str) -> None:
    """Placeholder email sender. Logs a warning and performs no action."""
    logger.warning(
        f"Default userdb email sender called for {to_email} with token {token}. "
        f"Path: {path}"
        f"Email not sent. Please override this dependency."
    )
    pass
