from functools import lru_cache
from typing import Mapping, Any
from wsgiref.validate import validator

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    API_BASE_URL: str

    TELEGRAM_API_TOKEN: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: str | None = None

    ALEMBIC_DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )

    @field_validator("DATABASE_URL", mode="before")  # type: ignore
    def assemble_postgres_db_url(cls, v: str | None, values: Any) -> str:
        """
        Assemble the PostgreSQL connection URL.

        If `DATABASE_URL` is not explicitly provided, this method constructs
        it using the other attributes such as host, port, username, password, and database name.

        Args:
            v (str | None): The value of the `DATABASE_URL` field.
            values (Any): A dictionary containing the other attributes of the settings.

        Returns:
            str: A fully assembled PostgreSQL connection URL.
        """
        if v and isinstance(v, str):
            return v
        return (
            f"postgresql+asyncpg://"
            f"{values.data['POSTGRES_USER']}:{values.data['POSTGRES_PASSWORD']}@"
            f"{values.data['POSTGRES_HOST']}:{values.data['POSTGRES_PORT']}/"
            f"{values.data['POSTGRES_DB']}"
        )

    @field_validator("ALEMBIC_DATABASE_URL", mode="before")  # type: ignore
    def assemble_alembic_postgres_db_url(cls, v: str | None, values: Any) -> str:
        """
        Assemble the PostgreSQL connection URL.

        If `DATABASE_URL` is not explicitly provided, this method constructs
        it using the other attributes such as host, port, username, password, and database name.

        Args:
            v (str | None): The value of the `DATABASE_URL` field.
            values (Any): A dictionary containing the other attributes of the settings.

        Returns:
            str: A fully assembled PostgreSQL connection URL.
        """
        if v and isinstance(v, str):
            return v
        return (
            f"postgresql+psycopg2://"
            f"{values.data['POSTGRES_USER']}:{values.data['POSTGRES_PASSWORD']}@"
            f"{values.data['POSTGRES_HOST']}:{values.data['POSTGRES_PORT']}/"
            f"{values.data['POSTGRES_DB']}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # noqa
