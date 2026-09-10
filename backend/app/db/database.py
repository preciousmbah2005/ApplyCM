"""Database engine and session factory.

Tuned for Neon: the compute endpoint scales to zero when idle, so pooled
connections can be severed between requests. `pool_pre_ping` validates a
connection before it is handed out, and `pool_recycle` retires sockets before
Neon's idle timeout can close them underneath us.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    connect_args={"connect_timeout": 10},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
