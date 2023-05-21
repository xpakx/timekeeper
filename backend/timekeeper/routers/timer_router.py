from fastapi import APIRouter
from .dto import timer_schemas
from ..services import timer_service

router = APIRouter(prefix="/timers")


@router.post("/", response_model=timer_schemas.TimerResponse)
async def add_timer(timer: timer_schemas.TimerRequest):
    return timer_service.add_timer(timer)


@router.get("/", response_model=list[timer_schemas.TimerResponse])
async def get_timers():
    return {"test": "all timers"}
