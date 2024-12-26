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
