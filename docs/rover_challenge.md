# Exmox Rover Challenge

This document focuses on the design and development of the Exmox Rover Challenge.
The high-level requirements are as follows:
- The robot is initialized with its current coordinates (X, Y) and the direction (NORTH, SOUTH, WEST, EAST) it is facing.
- The known obstacles are stored in the robot memory as a set of coordinates
- Endpoints:
  - return the current coordinates and direction as an JSON object
  - accepts a command string and returns the new position after execution


## Development

In the interest of simplicity, a virtual environment setup with a `requirements.txt` should get us started.
A tech stack of `FastAPI`, `SQLModel` and `PostgreSQL` is the recommended choice.
Therefore, a `docker-compose` setup should be best to create the `postgres` and `web` containers.
Tests should be run locally, and can use a more simplified setup using a local DB and `pytest`.


In the future, the setup can be extended to use `poetry` or similar to better handle dependencies and automate tasks.
The current setup will also afford flexibility between a `docker-compose` vs `kubernetes` approach.


## Datamodel

The suggested approach is to have two database models:
- `Rover`: maintains location coordinates i.e. (x, y) and direction i.e. N, E, S, W
- `Obstacle`: maintains coordinates (x, y) of all known obstacles on the moon

Rovers need a dedicated table to track the current location and direction of each rover.
In the future, there could be multiple rovers on the moon, and therefore each rover should have a `UUID`.
However, obstacles will be common to all rovers on the moon, and is therefore relevant information to all rovers.
A high-level sketch of the models is as follows:

```python
class Rover:
    uuid: UUID
    x: int
    y: int
    direction: Direction


class Obstacle:
    uuid: UUID
    x: int
    y: int
```

Other information such as whether or not a robot is "blocked" is subjective to the current existing fields.
Therefore, this information does not necessarily need to be tracked on a DB level.
The API endpoints to service requests can return this information after calculating the new rover positions.


## API Contracts

In order to facilitate versioning of endpoints, the prefix `/api/v1` is recommended.
The two necessary endpoints are described below:

### GET `/api/v1/rover`

The expected response would be 
```json
{
    "uuid": "a2ca5482-a14c-4955-9963-bf33e83eb8c2",
    "x": 1,
    "y": 3,
    "direction": "N"
}
```

### POST `/api/v1/rover/command`

The expected body would be
```json
{
  "command": "FLFFFRFLB"
}
```

The expected response would largely be the same as the GET endpoint, but with another flag to indicate if the robot's movement is blocked
```json
{
    "uuid": "a2ca5482-a14c-4955-9963-bf33e83eb8c2",
    "x": 1,
    "y": 3,
    "direction": "N",
    "stopped_due_to_obstacle": true
}
```