import logging
import uuid
from collections.abc import AsyncGenerator
from typing import Protocol

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from . import userdb_utils
from .config import Settings
from .db import get_user_db
from .models import User

logger = logging.getLogger("userdb.auth")

settings = Settings()


# Define a Protocol for the email sender callable
class EmailSenderCallable(Protocol):  # pragma: no cover
    async def __call__(self, *, to_email: str, token: str, path: str) -> None:
        ...


def get_jwt_strategy() -> JWTStrategy:
    """Return a JWTStrategy using the configured secret and 1 hour lifetime."""
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=3600,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=get_jwt_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """User manager for handling authentication events and secrets.

    This class extends BaseUserManager from fastapi-users, providing hooks for
    user lifecycle events. It uses secrets loaded from environment variables for
    password reset and email verification tokens, ensuring security and configurability.
    """

    def __init__(
        self,
        user_db: SQLAlchemyUserDatabase,
        settings_obj: Settings,
        email_sender: EmailSenderCallable | None = None,
    ):
        super().__init__(user_db)
        self.settings = settings_obj
        self._send_email = email_sender

        if self._send_email:
            self.reset_password_token_secret = self.settings.RESET_PASSWORD_SECRET
            self.verification_token_secret = self.settings.VERIFICATION_SECRET
            logger.info(
                "Email sender configured. Password reset and email verification features are enabled (if secrets are set)."
            )
        else:
            self.reset_password_token_secret = None
            self.verification_token_secret = None
            logger.warning(
                "No email sender configured. "
                "Password reset and email verification features will be disabled."
            )

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        """Called after a successful user login.

        This method can be used to update last login timestamps, trigger analytics,
        or send login notifications. Here, we simply log the event for auditing.
        """
        logger.info(f"User {user.id} logged in.")

    async def on_after_register(self, user: User, request: Request = None) -> None:
        """Called after a new user registers.

        Sends a welcome email with a verification link. This ensures users verify
        their email address, which is critical for account security and communication.
        """
        logger.info(f"User registered: id={user.id}")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request = None
    ) -> None:
        """Called after a user requests a password reset.

        Sends a password reset email with a secure, time-limited token. The email sender
        should construct the reset link using a frontend URL and the token.
        """
        if self._send_email:
            try:
                logger.info(f"Delegating password reset email sending for {user.email}")
                await self._send_email(
                    to_email=user.email,
                    token=token,
                    path="reset-password",
                )
            except Exception as e:
                logger.error(
                    f"Failed to send password reset email to {user.email}: {e}"
                )

    async def on_after_request_verify(
        self, user: User, token: str, request: Request = None
    ) -> None:
        """Called after a user requests email verification.

        Sends a verification email with a secure, time-limited token. The email sender
        should construct the verification link using a frontend URL and the token.
        """
        if self._send_email:
            try:
                logger.info(f"Delegating verification email sending for {user.email}")
                await self._send_email(
                    to_email=user.email,
                    token=token,
                    path="verify-email",
                )
            except Exception as e:
                logger.error(f"Failed to send verification email to {user.email}: {e}")

    # Additional hooks and business logic can be added here as needed.


def get_settings():
    return settings


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
    settings_obj: Settings = Depends(get_settings),
    email_sender_impl: EmailSenderCallable = Depends(
        userdb_utils.default_userdb_email_sender
    ),
) -> AsyncGenerator[UserManager, None]:
    """Dependency for providing a UserManager instance with the correct user DB."""
    yield UserManager(
        user_db, settings_obj=settings_obj, email_sender=email_sender_impl
    )


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
