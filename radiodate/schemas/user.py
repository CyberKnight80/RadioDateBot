from uuid import UUID

from pydantic import BaseModel


class UserView(BaseModel):
    id: UUID
    telegram_id: int

    name: str | None = None
    about: str | None = None
    avatar_url: str | None = None
    telegram_short_link: str | None = None


class UserUpdateView(BaseModel):
    name: str | None = None
    about: str | None = None
    avatar_url: str | None = None
    yandex_music_token: str | None = None
