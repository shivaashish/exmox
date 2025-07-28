from rover.datamodel.schemas.base import ModelBase
from rover.datamodel.schemas.fields import PrimaryKey


class _ObstacleBase(ModelBase):
    """Common base class for all obstacles"""

    uuid: PrimaryKey
    x: int
    y: int


class Obstacle(_ObstacleBase, table=True):
    """Model specific to the database"""


class ObstacleEntity(_ObstacleBase):
    """The entity returned from the db"""
