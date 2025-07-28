from fastapi import APIRouter

from .rover import router

core_router = APIRouter()

@core_router.get("/healthcheck/")
def healthcheck() -> str:
    return "OK"

core_router.include_router(router)
