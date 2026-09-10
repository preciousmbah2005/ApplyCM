import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/applycm")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super_secret_jwt_key_for_local_development_12345")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    STORAGE_URL: Optional[str] = os.getenv("STORAGE_URL", None)
    STORAGE_KEY: Optional[str] = os.getenv("STORAGE_KEY", None)

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()

