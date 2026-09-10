"""Application configuration.

Loads and validates every environment-provided setting exactly once at import
time. Any missing or insecure mandatory value raises immediately, so the
process crashes during boot rather than serving traffic in a degraded state.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final, Literal
from urllib.parse import urlsplit

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Anchored to the `backend/` package root so the file is found no matter which
# directory the process is launched from. A CWD-relative path would silently
# skip the file and crash boot when uvicorn is started from the repo root.
_ENV_FILE: Final[Path] = Path(__file__).resolve().parents[2] / ".env"

# Secrets that ship in examples/templates and must never reach a running app.
_FORBIDDEN_JWT_SECRETS: Final[frozenset[str]] = frozenset(
    {
        "placeholder_secret",
        "changeme",
        "change_me",
        "secret",
        "your_jwt_secret_key_here_must_be_long_and_random",
        "test",
    }
)

# HS256 keys shorter than this are brute-forceable; RFC 7518 requires >= 32 bytes.
_MIN_JWT_SECRET_LENGTH: Final[int] = 32

# psycopg2 only understands these; `postgres://` is a legacy alias it rejects.
_ALLOWED_DB_SCHEMES: Final[frozenset[str]] = frozenset(
    {"postgresql", "postgresql+psycopg2"}
)


class Settings(BaseSettings):
    """Strongly typed, fail-fast application settings."""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
        frozen=True,
    )

    # --- Mandatory: no defaults, so absence is a hard ValidationError. ---
    DATABASE_URL: str = Field(
        ...,
        min_length=1,
        description="PostgreSQL DSN for the Neon branch (psycopg2 driver).",
    )
    JWT_SECRET: str = Field(
        ...,
        min_length=1,
        description="HS256 signing key. Must be high-entropy and secret.",
    )

    # --- Optional, safely defaulted. ---
    JWT_ALGORITHM: Literal["HS256"] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, gt=0, le=1440)
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    CORS_ORIGINS: tuple[str, ...] = (
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    )

    @field_validator("JWT_SECRET")
    @classmethod
    def _reject_insecure_jwt_secret(cls, value: str) -> str:
        """Reject blank, well-known, or low-entropy signing keys."""
        secret = value.strip()

        if not secret:
            raise ValueError("JWT_SECRET must not be empty or whitespace.")

        if secret.lower() in _FORBIDDEN_JWT_SECRETS:
            raise ValueError(
                "JWT_SECRET matches a known placeholder value. Generate a real "
                "secret with: python -c \"import secrets; print(secrets.token_urlsafe(48))\""
            )

        if len(secret) < _MIN_JWT_SECRET_LENGTH:
            raise ValueError(
                f"JWT_SECRET must be at least {_MIN_JWT_SECRET_LENGTH} characters "
                f"(got {len(secret)}). Generate one with: "
                "python -c \"import secrets; print(secrets.token_urlsafe(48))\""
            )

        return secret

    @field_validator("DATABASE_URL")
    @classmethod
    def _validate_database_url(cls, value: str) -> str:
        """Ensure the DSN is a psycopg2-compatible PostgreSQL URL."""
        dsn = value.strip()

        if not dsn:
            raise ValueError("DATABASE_URL must not be empty or whitespace.")

        parts = urlsplit(dsn)

        if parts.scheme not in _ALLOWED_DB_SCHEMES:
            raise ValueError(
                f"DATABASE_URL scheme must be one of "
                f"{sorted(_ALLOWED_DB_SCHEMES)}; got '{parts.scheme or '<missing>'}'. "
                "Note that 'postgres://' is not accepted by psycopg2."
            )

        if not parts.hostname:
            raise ValueError("DATABASE_URL is missing a hostname.")

        if not parts.path.lstrip("/"):
            raise ValueError("DATABASE_URL is missing a database name.")

        return dsn

    @property
    def is_production(self) -> bool:
        """True when running under the production environment profile."""
        return self.ENVIRONMENT == "production"


def _load_settings() -> Settings:
    """Instantiate settings, converting Pydantic errors into a fatal boot error."""
    try:
        return Settings()  # pyright: ignore[reportCallIssue]
    except ValidationError as exc:
        details = "\n".join(
            f"  - {'.'.join(str(part) for part in error['loc']) or '<root>'}: {error['msg']}"
            for error in exc.errors()
        )
        message = (
            "\nFATAL: ApplyCM backend configuration is invalid.\n"
            f"{details}\n"
            "Set the required variables in backend/.env (see .env.example).\n"
        )
        print(message, file=sys.stderr)
        raise RuntimeError(message) from exc


settings: Final[Settings] = _load_settings()
