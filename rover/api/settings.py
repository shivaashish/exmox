import ast

from pydantic_settings import BaseSettings

from rover.datamodel import Direction


class Settings(BaseSettings):
    database_url: str
    start_position: str = "0,0"
    start_direction: str = "NORTH"
    obstacles: str = "[]"

    class Config:
        env_file = ".env"

    def get_start_position(self) -> tuple[int, int]:
        try:
            x, y = map(int, self.start_position.split(","))
            return x, y
        except ValueError:
            raise ValueError("Invalid start_position format. Expected 'x,y'")

    def get_start_direction(self) -> Direction:
        direction_map = {
            "NORTH": Direction.N,
            "EAST": Direction.E,
            "SOUTH": Direction.S,
            "WEST": Direction.W,
        }

        key = self.start_direction.strip().upper()
        if key not in direction_map:
            raise ValueError("Invalid start_direction. Must be one of NORTH, EAST, SOUTH, WEST")

        return direction_map[key]

    def get_obstacles(self) -> set[tuple[int, int]]:
        try:
            parsed = ast.literal_eval(self.obstacles)
            if not isinstance(parsed, list):
                raise ValueError
            return set(tuple(pair) for pair in parsed)
        except Exception:
            raise ValueError("Invalid OBSTACLES format. Expected format: [(x1,y1), (x2,y2), ...]")
