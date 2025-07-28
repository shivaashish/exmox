from enum import StrEnum

from pydantic import BaseModel

from rover.datamodel.schemas.base import ModelBase
from rover.datamodel.schemas.fields import PrimaryKey


class Direction(StrEnum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    def turn_left(self) -> "Direction":
        turns: dict[Direction, Direction] = {
            Direction.N: Direction.W,
            Direction.W: Direction.S,
            Direction.S: Direction.E,
            Direction.E: Direction.N,
        }
        return turns[self]

    def turn_right(self) -> "Direction":
        turns: dict[Direction, Direction] = {
            Direction.N: Direction.E,
            Direction.E: Direction.S,
            Direction.S: Direction.W,
            Direction.W: Direction.N,
        }
        return turns[self]


class CommandRequest(BaseModel):
    command: str


class _RoverBase(ModelBase):
    """Common base class for all rovers"""

    uuid: PrimaryKey
    x: int
    y: int
    direction: Direction

    def move_forward(self) -> None:
        match self.direction:
            case Direction.N:
                self.y += 1
            case Direction.S:
                self.y -= 1
            case Direction.E:
                self.x += 1
            case Direction.W:
                self.x -= 1

    def move_backward(self) -> None:
        match self.direction:
            case Direction.N:
                self.y -= 1
            case Direction.S:
                self.y += 1
            case Direction.E:
                self.x -= 1
            case Direction.W:
                self.x += 1

    def turn_left(self) -> None:
        self.direction = self.direction.turn_left()

    def turn_right(self) -> None:
        self.direction = self.direction.turn_right()


class Rover(_RoverBase, table=True):
    """Model specific to the database"""


class RoverEntity(_RoverBase):
    """The entity returned from the db"""
