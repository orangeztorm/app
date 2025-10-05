from functools import lru_cache  # caching decorator

from pydantic import Field  # field definitions with validation
from pydantic_settings import BaseSettings  # base class for settings management
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)  # async database engine
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.

    LEARN:
    - This class is part of the CONFIG layer.
    - It uses Pydantic for data validation and settings management.
    - Settings are immutable after initialization.
    """

    APP_NAME: str = "Auth Service"  # Name of the application
    ENV: str = "dev"
    PORT: int = 8000

    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./auth.db")

    JWT_SECRET: str = "change-me"  # should be overridden in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MIN: int = 60

    BCRYPT_ROUNDS: int = 12  # higher = more secure but slower
    REQUESTS_PER_MINUTE: int = 60  # simple rate limit knob

    class Config:
        env_file = ".env"  # load variables from .env file


@lru_cache()  # cache the settings instance
def get_settings() -> Settings:
    return Settings()


settings = get_settings()  # singleton settings instance

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENV == "dev",  # log SQL queries in dev mode
    pool_pre_ping=True,  # check if connections are alive
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
