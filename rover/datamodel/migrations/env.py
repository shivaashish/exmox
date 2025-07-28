from dotenv import load_dotenv
import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import SQLModel

load_dotenv()

from rover.datamodel.db import DATABASE_URL
from rover.datamodel.schemas import *  # noqa: F403

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        output_buffer=open(get_path_to_structure_file(), "w", encoding="utf-8"),
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    config_ini = config.get_section(config.config_ini_section)
    if config_ini is None:
        raise ValueError("No config.ini section found")

    connectable = engine_from_config(
        config_ini,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    if not database_exists(connectable.url):
        logging.warning("Creating the database now - first time deploying?")
        create_database(connectable.url)
    else:
        logging.info("Database already exists - running transactions now...")

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
