from radiodate.db.connection import db_session
from radiodate.models.base_models import BaseDatetimeModel
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, VARCHAR
from sqlalchemy import Column, func
from sqlalchemy import select, insert, update

from radiodate.schemas.user import UserView, UserUpdateView


class User(BaseDatetimeModel):
    __tablename__ = "users"

    telegram_id = Column("telegram_id", INTEGER, nullable=False)

    name = Column("name", VARCHAR(255), nullable=False)
    about = Column("about", VARCHAR(255), nullable=True)
    avatar_url = Column("avatar_url", TEXT, nullable=False)

    spotify_login = Column("spotify_login", TEXT, nullable=False)
    spotify_password = Column("spotify_password", TEXT, nullable=False)

    @classmethod
    async def get_random_user(cls) -> UserView:
        stmt = select(cls).order_by(func.random()).limit(1)
        result = await db_session.get().execute(stmt)
        random_row = result.scalars().first()
        return UserView.model_validate(random_row)

    @classmethod
    async def get_by_telegram_id(cls, telegram_id: int) -> UserView | None:
        query = select(cls).where(cls.telegram_id == telegram_id)
        result = await db_session.get().execute(query)
        result2 = result.scalars().first()
        if not result2:
            return None
        return UserView.model_validate(result2.as_dict())

    @classmethod
    async def create(cls, telegram_id: int):
        query = insert(cls).values(
            telegram_id=telegram_id,
            name="",
            about="",
            avatar_url="",
            spotify_login="",
            spotify_password="",
        )
        await db_session.get().execute(query)

    @classmethod
    async def update(cls, telegram_id: int, body: UserUpdateView):
        query = (
            update(cls)
            .where(cls.telegram_id == telegram_id)
            .values(telegram_id=telegram_id, **body.model_dump())
        )
        await db_session.get().execute(query)
