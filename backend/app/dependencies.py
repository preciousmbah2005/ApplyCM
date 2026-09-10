"""Shared FastAPI dependencies.

Provides the request-scoped database session and the authentication guard used
by every protected route. This is the only layer permitted to translate a token
into a persisted ``User``.
"""

from __future__ import annotations

import uuid
from collections.abc import Generator
from typing import Annotated, Final

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import verify_token
from app.db.database import SessionLocal
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# A single opaque 401 for every authentication failure mode. Distinguishing
# "no such user" from "bad signature" would leak account existence.
_CREDENTIALS_EXCEPTION: Final[HTTPException] = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db() -> Generator[Session, None, None]:
    """Yield a request-scoped SQLAlchemy session and always close it.

    Rolls back on an unhandled exception so a failed request can never leak a
    partially applied transaction into the connection pool.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
BearerToken = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(token: BearerToken, db: DbSession) -> User:
    """Resolve the authenticated user from a bearer token.

    The ``sub`` claim is required to be a UUID. Any other identifier form —
    notably an email address — is rejected outright, so the lookup path stays
    single-branch and the validation surface stays minimal.

    Raises:
        HTTPException: 401 if the token or subject is invalid, or the user is
            unknown; 403 if the account has been deactivated.
    """
    payload = verify_token(token)
    if payload is None:
        raise _CREDENTIALS_EXCEPTION

    subject = payload.get("sub")
    if not isinstance(subject, str):
        raise _CREDENTIALS_EXCEPTION

    try:
        user_id = uuid.UUID(subject)
    except ValueError:
        raise _CREDENTIALS_EXCEPTION from None

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise _CREDENTIALS_EXCEPTION

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
