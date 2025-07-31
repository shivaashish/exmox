from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as SessionType
from sqlmodel import select

from rover.datamodel import (CommandRequest, Obstacle, Rover, RoverEntity,
                             session_generator)

Session = Annotated[SessionType, Depends(session_generator)]
router = APIRouter(prefix="/rover", tags=["rover"])


@router.get("/")
def get_current_location(session: Session) -> RoverEntity:
    db_obj = session.exec(select(Rover)).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Rover not found")

    return RoverEntity.model_validate(db_obj)


@router.post("/command")
def move_after_command(request: CommandRequest, session: Session) -> dict:
    db_obj = session.exec(select(Rover)).first()
    if not db_obj:
        raise HTTPException(status_code=404, detail="Rover not found")

    obstacles = {(obs.x, obs.y) for obs in session.exec(select(Obstacle)).all()}
    stopped_due_to_obstacle = False

    for action in request.command.upper():
        prev_x, prev_y = db_obj.x, db_obj.y

        if action == "F":
            db_obj.move_forward()
        elif action == "B":
            db_obj.move_backward()
        elif action == "L":
            db_obj.turn_left()
        else:
            db_obj.turn_right()

        # Check for obstacle and revert
        if action in {"F", "B"} and (db_obj.x, db_obj.y) in obstacles:
            db_obj.x, db_obj.y = prev_x, prev_y
            stopped_due_to_obstacle = True
            break

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    result = RoverEntity.model_validate(db_obj).model_dump()
    result["stopped_due_to_obstacle"] = stopped_due_to_obstacle
    return result
