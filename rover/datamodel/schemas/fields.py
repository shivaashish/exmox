from typing import Annotated
from uuid import UUID, uuid4

from sqlmodel import Field

# A UUID field used as a primary key.
PrimaryKey = Annotated[UUID, Field(primary_key=True, default_factory=uuid4)]
