# userdb

[![Python Versions](https://img.shields.io/pypi/pyversions/beanone-userdb)](https://pypi.org/project/beanone-userdb)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Tests](https://github.com/beanone/userdb/actions/workflows/tests.yml/badge.svg)](https://github.com/beanone/userdb/actions?query=workflow%3Atests)
[![Coverage](https://codecov.io/gh/beanone/userdb/branch/main/graph/badge.svg)](https://codecov.io/gh/beanone/userdb)
[![Code Quality](https://img.shields.io/badge/code%20style-ruff-000000)](https://github.com/astral-sh/ruff)
[![PyPI version](https://img.shields.io/pypi/v/beanone-userdb)](https://pypi.org/project/beanone-userdb)

## Features

- User model and schema library for authentication services
- Designed for integration with FastAPI and fastapi-users
- Reusable across multiple services
- Internal async API key management (CRUD) module

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Key Management](#api-key-management)
- [Architecture & Integration Guide](#architecture--integration-guide)
- [User Model & Database Schema](#user-model--database-schema)
- [Configuration Usage](#configuration-usage)
- [Testing](#testing)
- [Setting Up the User Database](#setting-up-the-user-database)
- [Admin User Account Setup](#admin-user-account-setup)
- [License](#license)

## Installation

```bash
pip install beanone-userdb
```

## Usage

```python
from userdb.models import User
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from userdb.db import get_async_session

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: str, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        User.__table__.select().where(User.id == user_id)
    )
    user = result.fetchone()
    if user:
        return user
    return {"error": "User not found"}
```

## API Key Management

userdb includes an internal API key management module (`userdb.apikey_manager`) that provides async functions for creating, listing, and deleting API keys. These functions encapsulate all business logic and database operations for API key management and are intended for use within the userdb codebase.

- `create_api_key(user_id, service_id, session, name=None, expires_at=None)`
- `list_api_keys(user_id, session)`
- `delete_api_key(key_id, user_id, session)`

All functions are async and require an `AsyncSession` for database access.

## Architecture & Integration Guide

### Typical Architecture

A recommended architecture for a login/authentication service using `userdb`:

```mermaid
graph TD
    A[Client App / Frontend]
    B[API Gateway / HTTPS Proxy]
    C[FastAPI Login Service - uses userdb]
    D[Database - PostgreSQL, etc.]
    A --> B
    B --> C
    C --> D
```

- **userdb** provides the user model, schemas, and authentication logic.
- The login service is a FastAPI app that imports userdb and wires up routers.
- Other services can import userdb to share the user model and schemas for consistent user data handling.

### Example FastAPI Login Service

```python
from fastapi import FastAPI
from userdb.auth import auth_backend, fastapi_users, get_user_manager
from userdb.schemas import UserRead, UserCreate

app = FastAPI()

# Auth routes
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserRead), prefix="/users", tags=["users"])
```

### Configuring Email Sending (for Password Reset & Verification)

The `userdb` library's `UserManager` supports sending emails for password resets and email verifications. This feature is optional and depends on you providing an email sending implementation.

**1. Email Sender Interface:**

`userdb` defines a protocol for the email sender:
```python
# userdb.auth.EmailSenderCallable
class EmailSenderCallable(Protocol):
    async def __call__(self, *, to_email: str, token: str, path: str) -> None:
        # path will be a string like "reset-password" or "verify-email"
        ...
```
Your custom email sender function must match this signature. It will receive:
- `to_email`: The recipient's email address.
- `token`: The generated token for the action.
- `path`: A string indicating the type of action (e.g., "reset-password", "verify-email"). This helps your sender construct the correct link and email content.

Your implementation is responsible for:
- Using the `path` to determine the email's purpose (password reset or verification) and tailor the subject and body accordingly.
- Using the provided `token`, the `path`, and your application's `frontend_url` (from your own settings) to create the full, clickable link within the email body (e.g., `f"{frontend_url}/{path}?token={token}"`).
- Actually sending the email using your preferred email service (e.g., SendGrid, SES, SMTP).

**2. Default Placeholder:**

By default, `userdb` uses a placeholder email sender that logs a warning and does not send any emails. This is located at `userdb.userdb_utils.default_userdb_email_sender`. Its signature now also includes the `path` argument.

**3. Enabling Email Features:**

For password reset and email verification features to be enabled in `userdb` (and for `fastapi-users` to expose the related routes):
- You **must** provide a working email sender implementation that conforms to the `EmailSenderCallable` protocol.
- Your `userdb.config.Settings` object (or a subclass used by your application) **must** have the `RESET_PASSWORD_SECRET` and `VERIFICATION_SECRET` attributes set (they default to `JWT_SECRET` if not explicitly provided).

**4. Injecting Your Custom Email Sender:**

To use your own email sending logic, you'll override the default dependency in your FastAPI application setup:

```python
# In your main FastAPI application file (e.g., app/main.py or src/your_project/main.py)
from fastapi import FastAPI
from userdb.auth import fastapi_users, auth_backend # From userdb library
from userdb.schemas import UserRead, UserCreate    # From userdb library
from userdb import userdb_utils                    # To access the default sender for overriding

# 1. Define your custom email sender function
# (This could be in a separate services/email.py module in your project)
async def my_custom_email_sender(*, to_email: str, token: str, path: str) -> None:
    # Example: (Replace with your actual email sending logic)
    # from your_project.config import my_app_settings # Your app's specific settings
    # frontend_url = my_app_settings.FRONTEND_APP_URL
    # full_link = f"{frontend_url}/{path}?token={token}"

    subject = ""
    body_intro = ""
    frontend_url = "https://your-frontend.com" # Replace with your actual frontend URL from settings
    action_link = f"{frontend_url}/{path}?token={token}"

    if path == "reset-password":
        subject = "Reset Your Password"
        body_intro = "Please click the link below to reset your password:"
    elif path == "verify-email":
        subject = "Verify Your Email Address"
        body_intro = "Please click the link below to verify your email address:"
    else:
        subject = "Important Account Action"
        body_intro = "Please click the link below:"

    email_body = f"{body_intro}\n{action_link}"

    print(f"Simulating email to: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body: {email_body}")
    # Your actual email sending code using a service like SendGrid, SES, or SMTP would go here

app = FastAPI()

# 2. Override the default email sender dependency
app.dependency_overrides[userdb_utils.default_userdb_email_sender] = my_custom_email_sender

# 3. Include fastapi-users routers (these will now use your_custom_email_sender)
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserRead), prefix="/users", tags=["users"])

# Add password reset and verification routers from fastapi-users
# These will only be active if the corresponding secrets are set in UserManager
# (which depends on an email_sender being configured)
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])

# Your application's settings (e.g., from userdb.config.Settings or a subclass)
# should define its own FRONTEND_APP_URL if your custom email sender needs it for link construction.
# userdb's UserManager enables password/verification features if an email_sender
# is provided and the necessary token secrets are available.
```

**Important Note on Email Content:**
(This paragraph can be removed or simplified as the `path` argument now helps differentiate)

This setup ensures that `userdb` remains decoupled from specific email sending implementations and URL structures, while providing the necessary hooks for downstream applications to integrate their own email services.

### Environment Variables (Required for Production)
- `JWT_SECRET`: Secret key for JWT signing (**required**; application will raise an error if not set)
- `RESET_PASSWORD_SECRET`: Secret for password reset tokens (optional, defaults to JWT secret)
- `VERIFICATION_SECRET`: Secret for verification tokens (optional, defaults to JWT secret)
- `DATABASE_URL`: SQLAlchemy DB URL (e.g., `postgresql+asyncpg://user:pass@host/dbname`)

> **Note:** If `JWT_SECRET` is not set, the application will raise a `RuntimeError` at startup.

### Security & Deployment Best Practices
- **CORS:** Configure CORS in your FastAPI app using `CORSMiddleware` to restrict allowed origins.
- **HTTPS:** Always deploy behind a TLS-terminating proxy (e.g., NGINX, Caddy, cloud load balancer).
- **Secret Management:** Never hardcode secrets. Use environment variables or a secrets manager.
- **Rate Limiting:** Add rate limiting at the API gateway or with middleware to prevent brute-force attacks.
- **Email Verification:** Enable and configure email verification in your login service for new users.
- **Audit Logging:** Log authentication events for security monitoring.

### Extending the User Model
- You can add fields to the `User` model and corresponding Pydantic schemas in your own code or by forking/extending userdb.
- All models and schemas use type annotations and are compatible with FastAPI and Pydantic.

### User Model & Database Schema

#### Default User Model Fields

| Field            | Type      | Description                 | Required | Notes                |
|------------------|-----------|-----------------------------|----------|----------------------|
| id               | UUID      | Unique user identifier      | Yes      | Primary key          |
| email            | str       | User email (unique)         | Yes      | Unique, indexed      |
| hashed_password  | str       | Hashed password             | Yes      | Not exposed in API responses |
| full_name        | str/None  | User's full name            | No       | Optional             |
| is_active        | bool      | Is the user active?         | Yes      |                      |
| is_superuser     | bool      | Is the user an admin?       | Yes      |                      |
| is_verified      | bool      | Has the user verified email | Yes      |                      |

> **Note:** The table is named `"user"`, which is a reserved word in some databases (e.g., PostgreSQL). Consider renaming to `"users"` if you encounter issues.

#### Example User Schema

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "User Name",
  "is_active": true,
  "is_superuser": false,
  "is_verified": true
}
```

#### Extending the User Model
- To add fields, update the `User` SQLAlchemy model and the corresponding Pydantic schemas.
- Run a new Alembic migration to update the database schema.
- Update the UI to handle new fields as needed.
- Keep the UI and backend in sync regarding user data shape.
- **Tip:** If you need roles or permissions, add fields (e.g., `role`, `permissions`) to the model and schemas, and update your business logic accordingly.

### Configuration Usage

The `userdb.config.Settings` class provides all configuration via environment variables or a `.env` file. **There is no longer a global `settings` singleton.**

- To use configuration, import and instantiate `Settings` directly:

```python
from userdb.config import Settings
settings = Settings()
```

- If you are building a service that needs additional configuration, subclass `Settings`:

```python
from userdb.config import Settings as UserdbSettings

class MyServiceSettings(UserdbSettings):
    MY_SERVICE_API_KEY: str

settings = MyServiceSettings()
```

- All environment variables must be set before instantiating `Settings`.
- `JWT_SECRET` **must** be set, or a `RuntimeError` will be raised at startup.

### Testing
- The test suite sets `JWT_SECRET` automatically for all tests (see `tests/conftest.py`).
- All code and tests should instantiate `Settings` directly as needed.
- There is no global singleton; each test or module should create its own `Settings` instance if configuration is needed.
- See `tests/unit/test_userdb.py` and `tests/unit/test_apikey_manager.py` for example tests and mocking patterns.

### Setting Up the User Database

Before running your login service, you need to ensure the user table exists in your database.

#### Recommended: Use Alembic for Migrations
For production and team environments, use [Alembic](https://alembic.sqlalchemy.org/) to manage database migrations:

```bash
alembic revision --autogenerate -m "create user table"
alembic upgrade head
```

Make sure your Alembic `env.py` includes the userdb model's metadata:
```python
from userdb.models import Base

target_metadata = Base.metadata
```

#### Quick Local Setup: Create Tables Programmatically
For local development or quick tests, you can create the tables directly using SQLAlchemy:

```python
from userdb.models import Base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./test.db")  # Or your DB URL
Base.metadata.create_all(engine)
```

> **Note:** For production, always use migrations to avoid data loss and ensure schema consistency.

### Admin User Account Setup

After the user tables are created (either via Alembic or programmatically), `userdb` will automatically create an admin (superuser) account if one does not already exist. This ensures you always have an initial admin user for your application.

**Default admin credentials:**
- Email: `admin@example.com`
- Password: `changeme`
- Full name: `Admin`

**Override defaults in production:**
Set the following environment variables before starting your app to change the admin account credentials:
- `ADMIN_EMAIL` (default: `admin@example.com`)
- `ADMIN_PASSWORD` (default: `changeme`)
- `ADMIN_FULL_NAME` (default: `Admin`)

> **Security Note:** Always override the default admin password and email in production environments!

The admin user is created only if no superuser exists in the database. If you delete the admin user, it will be recreated on the next app startup unless another superuser exists.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
