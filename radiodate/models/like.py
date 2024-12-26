import uuid

from radiodate.db.connection import db_session
from radiodate.models.base_models import BaseModel
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa


class Like(BaseModel):
    __tablename__ = "likes"

    liker = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        default=uuid.uuid4,
        unique=True,
    )
    liked = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        default=uuid.uuid4,
        unique=True,
    )

    @classmethod
    async def get_rel(
        cls, liker_user_id: uuid.UUID, liked_user_id: uuid.UUID
    ) -> "Like":
        query = sa.select(cls).where(
            (cls.liker == liker_user_id) & (cls.liked == liked_user_id)
        )
        result = (await db_session.get().execute(query)).scalars().first()
        return result

    @classmethod
    async def like(cls, liker_user_id: uuid.UUID, liked_user_id: uuid.UUID) -> None:
        query = sa.insert(cls).values(liker=liker_user_id, liked=liked_user_id)
        await db_session.get().execute(query)

    @classmethod
    async def get_match(cls, user_id: uuid.UUID) -> uuid.UUID | None:
        l1 = sa.alias(cls)
        l2 = sa.alias(cls)

        query = (
            sa.select(l2.c.liker)
            .where(
                sa.and_(
                    l1.c.liker == l2.c.liked,  # Взаимный лайк
                    l1.c.liked == l2.c.liker,  # Взаимный лайк
                    l1.c.liker == user_id,  # Исходящий лайк от текущего пользователя
                )
            )
            .limit(1)
        )

        result = await db_session.get().execute(query)
        matching_user = (
            result.scalar()
        )  # Получаем ID пользователя, который поставил взаимный лайк
        return matching_user

    @classmethod
    async def delete_match(cls, user_id: uuid.UUID, matched_user_id: uuid.UUID) -> None:
        query = sa.delete(cls).where(
            sa.or_(
                sa.and_(
                    cls.liker == user_id, cls.liked == matched_user_id
                ),  # Исходящий лайк
                sa.and_(
                    cls.liker == matched_user_id, cls.liked == user_id
                ),  # Входящий лайк
            )
        )
        await db_session.get().execute(query)
