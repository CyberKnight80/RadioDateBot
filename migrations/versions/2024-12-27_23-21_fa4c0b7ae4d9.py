"""remove spotify add yandex

Revision ID: fa4c0b7ae4d9
Revises: 389add41e70f
Create Date: 2024-12-27 23:21:33.135586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa4c0b7ae4d9'
down_revision: Union[str, None] = '389add41e70f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('yandex_music_token', sa.TEXT(), nullable=True))
    op.drop_column('users', 'spotify_password')
    op.drop_column('users', 'spotify_login')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('spotify_login', sa.TEXT(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('spotify_password', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('users', 'yandex_music_token')
    # ### end Alembic commands ###