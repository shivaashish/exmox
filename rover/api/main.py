from contextlib import AbstractAsyncContextManager, asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel, select

from rover.api.routers import core_router
from rover.api.settings import Settings
from rover.datamodel import Obstacle, Rover, session_generator


@asynccontextmanager
async def lifespan(app: FastAPI) -> AbstractAsyncContextManager:
    settings = Settings()
    rover_x, rover_y = settings.get_start_position()
    obstacles = settings.get_obstacles()
    direction = settings.get_start_direction()

    with next(session_generator()) as session:
        if not session.exec(select(Rover)).first():
            rover = Rover(x=rover_x, y=rover_y, direction=direction)
            session.add(rover)

        if not session.exec(select(Obstacle)).all():
            for x, y in obstacles:
                db_obstacle = Obstacle(x=x, y=y)
                session.add(db_obstacle)

        session.commit()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(core_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(f"{Path(__file__).stem}:app", host="0.0.0.0", port=8000, reload=True)
