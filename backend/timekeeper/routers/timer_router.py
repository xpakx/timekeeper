from fastapi import APIRouter
from .dto import timer_request
from ..services import timer_service

router = APIRouter(prefix="/timers")


@router.post("/")
async def add_timer(timer: timer_request.TimerRequest):
    timer_service.add_timer(timer)
    return {"test": "timer path"}


@router.get("/")
async def get_timers():
    return {"test": "all timers"}
