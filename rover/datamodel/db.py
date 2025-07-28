import json
import os
from functools import partial
from typing import Any, Callable, Iterator

from pydantic_core import to_jsonable_python
from sqlmodel import Session, create_engine

DATABASE_URL = os.environ["DATABASE_URL"]

SessionFactory = Callable[[], Session]


def custom_serializer(value: Any) -> str:  # noqa: ANN401
    return json.dumps(value, default=partial(to_jsonable_python, by_alias=False))


engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True, json_serializer=custom_serializer)


def session_generator() -> Iterator[Session]:
    with Session(engine, autoflush=False) as session:
        yield session


def get_session() -> Session:
    """Utility function to return a session for the default engine"""

    return Session(engine, autoflush=False)
