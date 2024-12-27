from uuid import UUID

from pydantic import BaseModel


class UserView(BaseModel):
    id: UUID
    telegram_id: int

    name: str | None = None
    about: str | None = None
    avatar_url: str | None = None
    telegram_short_link: str | None = None

    album_cover_url: str | None = None
    match_percent: str | None = None
    is_matched: bool = False

    class Config:
        orm_mode = True


class UserUpdateView(BaseModel):
    name: str | None = None
    about: str | None = None
    avatar_url: str | None = None
    yandex_music_token: str | None = None
