from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import select, Session, SQLModel, create_engine

from rover.api.main import app
from rover.datamodel import Direction, Obstacle, Rover, session_generator

test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
connection = test_engine.connect()
transaction = connection.begin()

SessionLocal = sessionmaker(bind=connection, class_=Session, expire_on_commit=False)


@pytest.fixture(scope="module", autouse=True)
def setup_db() -> Generator:
    SQLModel.metadata.create_all(bind=connection)

    app.dependency_overrides[session_generator] = lambda: SessionLocal()

    with SessionLocal() as session:
        session.add(Rover(x=2, y=0, direction=Direction.S))
        for x, y in [(1, 4), (3, 5), (7, 4)]:
            session.add(Obstacle(x=x, y=y))
        session.commit()
    yield

    transaction.rollback()
    connection.close()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestRoverAPI:
    def test_get_rover_location(self, client: TestClient) -> None:
        response = client.get("api/v1/rover/")
        assert response.status_code == 200

        data = response.json()
        assert data["x"] == 2
        assert data["y"] == 0
        assert data["direction"] == "S"

    def test_move_rover_without_obstacle(self, client: TestClient) -> None:
        response = client.post("api/v1/rover/command", json={"command": "R"})
        assert response.status_code == 200

        data = response.json()
        assert data["direction"] == "W"
        assert data["stopped_due_to_obstacle"] is False

    def test_move_rover_into_obstacle(self, client: TestClient) -> None:
        with Session(test_engine) as session:
            rover = session.exec(select(Rover)).first()
            rover.x, rover.y = 1, 3
            rover.direction = Direction.N
            session.add(rover)
            session.commit()

        response = client.post("api/v1/rover/command", json={"command": "F"})
        assert response.status_code == 200

        data = response.json()
        assert data["x"] == 1
        assert data["y"] == 3
        assert data["stopped_due_to_obstacle"] is True

    def test_invalid_command(self, client: TestClient) -> None:
        response = client.post("api/v1/rover/command", json={"command": "FX"})
        assert response.status_code == 400
        assert "Invalid command" in response.json()["detail"]
