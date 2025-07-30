import uuid
from datetime import UTC, datetime
from enum import Enum

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Index, String, event
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class User(SQLAlchemyBaseUserTableUUID, Base):  # type: ignore[misc, valid-type]
    """
    User model with user_id_str logic:
    - Always set by a before_insert event in Python for all DBs.
    - In Postgres, a DB trigger also sets it for extra safety.
    Do not update user_id_str elsewhere.
    """

    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=True)
    user_id_str = Column(String(36), unique=True, nullable=False)


@event.listens_for(User, "before_insert")
def set_user_id_str(mapper, connection, target: User) -> None:
    """Set user_id_str before insert if not already set."""
    if not target.id:
        target.id = uuid.uuid4()
    target.user_id_str = str(target.id)


class APIKeyStatus(str, Enum):
    """Enum for API key status values."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    REVOKED = "revoked"
    EXPIRED = "expired"


class APIKey(Base):
    """
    API Key model for managing user API keys.

    Attributes:
        id: Unique identifier for the API key
        user_id: Foreign key to the user who owns this key
        key_hash: Hashed version of the API key
        name: Optional name for the API key
        created_at: Timestamp when the key was created
        service_id: Identifier for the service this key is associated with
        status: Current status of the API key (active/inactive/revoked/expired)
        expires_at: Optional timestamp when the key expires
        last_used_at: Timestamp of the last time the key was used
    """

    __tablename__ = "api_keys"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        String(36), ForeignKey("user.user_id_str", ondelete="CASCADE"), nullable=False
    )
    key_hash = Column(String, nullable=False, unique=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now(UTC))
    service_id = Column(String, nullable=False)
    status = Column(SQLEnum(APIKeyStatus), default=APIKeyStatus.ACTIVE, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    __table_args__ = (Index("ix_api_keys_user_id", "user_id"),)

    def __init__(
        self,
        user_id: str,
        key_hash: str,
        service_id: str,
        name: str | None = None,
        status: APIKeyStatus = APIKeyStatus.ACTIVE,
        expires_at: datetime | None = None,
        last_used_at: datetime | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        """
        Initialize a new API key.

        Args:
            user_id: String version of the user's UUID
            key_hash: Hashed version of the API key
            service_id: Identifier for the service this key is associated with
            name: Optional name for the API key
            status: Current status of the API key
            expires_at: Optional timestamp when the key expires
            last_used_at: Timestamp of the last time the key was used
            id: Optional custom ID for the key
            created_at: Optional custom creation timestamp

        Raises:
            ValueError: If service_id is empty
        """
        if not service_id:
            raise ValueError("service_id is required for APIKey")
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.key_hash = key_hash
        self.name = name
        self.created_at = created_at or datetime.now(UTC)
        self.service_id = service_id
        self.status = status
        self.expires_at = expires_at
        self.last_used_at = last_used_at
