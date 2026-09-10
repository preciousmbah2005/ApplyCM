from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/applycm"
    JWT_SECRET: str = "placeholder_secret"
    JWT_ALGORITHM: str = "HS256"
    STORAGE_URL: Optional[str] = None
    STORAGE_KEY: Optional[str] = None

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()
