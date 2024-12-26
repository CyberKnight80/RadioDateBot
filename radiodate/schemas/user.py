from uuid import UUID

from pydantic import BaseModel


class UserView(BaseModel):
    id: UUID
    telegram_id: int

    name: str | None = None
    about: str | None = None
    avatar_url: str | None = None


class UserUpdateView(BaseModel):
    name: str | None = None
    about: str | None = None
    avatar_url: str | None = None

    spotify_login: str | None = None
    spotify_password: str | None = None
