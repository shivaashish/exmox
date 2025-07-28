# Exmox Rover Challenge

## Setup

Local setup strongly recommends usage of a virtual environment, the choice of which is left to the user.

To run the rover challenge, a `docker-compose` setup is used.
This can be spun up using the command
```commandline
docker-compose up --build -d
```

Container logs can be viewed using the command
```commandline
docker-compose logs web
```

The setup can be torn down using
```commandline
docker-compose down -v
```

Initial coordinates for the robot are initialized using environment variables, defined in the `.env` file.
The `-v` flag tears down the postgres volumes, and should be done to reset the robot to the original settings in the `.env` file.
If not, the previous state of the rover is persisted i.e. any results from movement commands will be persisted.


## Endpoints

To query the FastAPI server, requests can be made to
- `http://localhost:8000/api/v1/healthcheck`
- `http://localhost:8000/api/v1/rover`
- `http://localhost:8000/api/v1/rover/command`

Refer to the draft in the `/docs` folder for a detailed breakdown of the expected request bodies and responses.


## Testing

Tests are run using `sqlite`, and the `DATABASE_URL` is defined in the `.env` file.
In order to run tests, run the following command from within the virtual environment.
```commandline
pytest
```


## Type checks and linting

Ruff and isort are used for linting.
Run these commands from project root as follows:

```commandline
isort .
ruff check . --select ANN
```