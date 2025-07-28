from __future__ import annotations

from pydantic.alias_generators import to_camel as pydantic_to_camel
from sqlmodel import SQLModel
from sqlmodel._compat import SQLModelConfig  # noqa: PLC2701


def to_camel(x: str) -> str:
    """Convert from snake_case to camelCase for serialization (output)."""
    return pydantic_to_camel(x).replace("__", "")


class ModelBase(SQLModel):
    model_config = SQLModelConfig(alias_generator=to_camel, populate_by_name=True)
