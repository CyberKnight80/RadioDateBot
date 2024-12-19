from pydantic import BaseModel


class UserView(BaseModel):
    telegram_id: int

    name: str | None = None
    about: str | None = None
    avatar_url: str | None = None

    spotify_login: str | None = None
    spotify_password: str | None = None
