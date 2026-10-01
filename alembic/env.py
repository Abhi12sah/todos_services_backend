from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.db.base import Base
from app.models import User, Todo
from app.config import settings


# Alembic configuration object
config = context.config


# Get database URL from our application settings
database_url = settings.database_url.render_as_string(
    hide_password=False
)

# Give the database URL to Alembic
config.set_main_option(
    "sqlalchemy.url",
    database_url.replace("%", "%%")
)


# Configure Python logging using alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Tell Alembic about our SQLAlchemy models
target_metadata = Base.metadata


def run_migrations_offline() -> None:
   

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
  
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Decide which migration mode Alembic should use
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()