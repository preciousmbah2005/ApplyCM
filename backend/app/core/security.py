"""Security primitives: password hashing and JWT encode/decode.

This module is intentionally free of FastAPI, SQLAlchemy, and request-scope
concerns. It exposes pure functions so the service and dependency layers can
compose them without inheriting web-framework coupling.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Final

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings

# bcrypt truncates silently past 72 bytes; we reject instead of truncating so
# two different long passwords can never collide into the same hash.
_BCRYPT_MAX_PASSWORD_BYTES: Final[int] = 72

_TOKEN_TYPE_ACCESS: Final[str] = "access"

ACCESS_TOKEN_EXPIRE_MINUTES: Final[int] = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class InvalidPasswordError(ValueError):
    """Raised when a password cannot be hashed (e.g. it exceeds bcrypt's limit)."""


class TokenSubjectError(ValueError):
    """Raised when a token subject is not a valid UUID."""


# --------------------------------------------------------------------------- #
# Password hashing
# --------------------------------------------------------------------------- #
def get_password_hash(password: str) -> str:
    """Hash a plaintext password with a per-password bcrypt salt.

    Raises:
        InvalidPasswordError: If the password is empty or exceeds 72 bytes.
    """
    if not password:
        raise InvalidPasswordError("Password must not be empty.")

    password_bytes = password.encode("utf-8")

    if len(password_bytes) > _BCRYPT_MAX_PASSWORD_BYTES:
        raise InvalidPasswordError(
            f"Password must not exceed {_BCRYPT_MAX_PASSWORD_BYTES} bytes "
            f"when UTF-8 encoded (got {len(password_bytes)})."
        )

    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Constant-time comparison of a plaintext password against a bcrypt hash.

    Returns False rather than raising, so callers cannot distinguish a malformed
    stored hash from a wrong password via exception behaviour.
    """
    if not plain_password or not hashed_password:
        return False

    password_bytes = plain_password.encode("utf-8")

    if len(password_bytes) > _BCRYPT_MAX_PASSWORD_BYTES:
        return False

    try:
        return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
    except (ValueError, TypeError):
        # Malformed or non-bcrypt hash stored in the column.
        return False


# --------------------------------------------------------------------------- #
# JWT
# --------------------------------------------------------------------------- #
def _coerce_subject(subject: Any) -> str:
    """Normalise a token subject to its canonical UUID string form.

    Raises:
        TokenSubjectError: If the subject is not a valid UUID.
    """
    if isinstance(subject, uuid.UUID):
        return str(subject)

    if not isinstance(subject, str):
        raise TokenSubjectError(
            f"Token subject must be a UUID or UUID string, got {type(subject).__name__}."
        )

    try:
        return str(uuid.UUID(subject))
    except ValueError as exc:
        raise TokenSubjectError(
            "Token subject must be a valid UUID string; "
            "email addresses and other identifiers are not accepted."
        ) from exc


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Mint a signed HS256 access token.

    The ``sub`` claim is mandatory and must be a UUID, which guarantees the
    dependency guard never has to interpret an ambiguous subject.

    Raises:
        TokenSubjectError: If ``sub`` is absent or is not a valid UUID.
    """
    if "sub" not in data:
        raise TokenSubjectError("Token payload must include a 'sub' claim.")

    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    claims: dict[str, Any] = {
        **data,
        "sub": _coerce_subject(data["sub"]),
        "iat": now,
        "exp": expire,
        "jti": str(uuid.uuid4()),
        "typ": _TOKEN_TYPE_ACCESS,
    }

    return jwt.encode(
        claims,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def verify_token(token: str) -> dict[str, Any] | None:
    """Decode and validate an access token.

    Returns the claims on success, or ``None`` if the token is malformed,
    expired, wrongly signed, of the wrong type, or carries a non-UUID subject.
    """
    if not token:
        return None

    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"require_exp": True, "require_sub": True},
        )
    except JWTError:
        return None

    if payload.get("typ") != _TOKEN_TYPE_ACCESS:
        return None

    try:
        payload["sub"] = _coerce_subject(payload.get("sub"))
    except TokenSubjectError:
        return None

    return payload


def get_subject_uuid(token: str) -> uuid.UUID | None:
    """Return the validated UUID subject of a token, or ``None`` if invalid."""
    payload = verify_token(token)
    if payload is None:
        return None

    try:
        return uuid.UUID(str(payload["sub"]))
    except (ValueError, KeyError):
        return None
