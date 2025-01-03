"""empty message

Revision ID: bddc0ef5e7ac
Revises: 
Create Date: 2024-12-20 01:22:46.761360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bddc0ef5e7ac'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('telegram_id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
    sa.Column('about', sa.VARCHAR(length=255), nullable=True),
    sa.Column('avatar_url', sa.TEXT(), nullable=False),
    sa.Column('spotify_login', sa.TEXT(), nullable=False),
    sa.Column('spotify_password', sa.TEXT(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
