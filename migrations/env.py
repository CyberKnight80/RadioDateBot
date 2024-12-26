# noqa: E401
from alembic import context
from sqlalchemy import create_engine

from radiodate.models.user import BaseDatetimeModel, User

from radiodate.settings import get_settings
from radiodate.db.base import Base

config = context.config


def include_object(object, name, type_, reflected, compare_to):

    if type_ == "column" and object.info.get("skip_autogenerate", False):
        return False

    return True


def run_migrations_online() -> None:
    engine = create_engine(get_settings().ALEMBIC_DATABASE_URL)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            compare_type=True,
            include_object=include_object,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
