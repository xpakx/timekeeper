from fastapi import APIRouter, Depends
from .dto import timer_schemas
from ..services import timer_service
from typing import Annotated
from ..security.jwt import get_current_user, CurrentUser

router = APIRouter(prefix="/timers")


@router.post("/", response_model=timer_schemas.TimerResponse)
async def add_timer(
        timer: timer_schemas.TimerRequest,
        username: Annotated[CurrentUser, Depends(get_current_user)]
        ):
    return timer_service.add_timer(timer)


@router.get("/", response_model=list[timer_schemas.TimerResponse])
async def get_timers(
        username: Annotated[CurrentUser, Depends(get_current_user)],
        page: int = 0,
        size: int = 20,
        ):
    return timer_service.get_timers(page, size)


@router.put("/{id}", response_model=timer_schemas.TimerResponse)
async def edit_timer(
        id: int,
        timer: timer_schemas.TimerRequest,
        username: Annotated[CurrentUser, Depends(get_current_user)]
        ):
    return timer_service.edit_timer(id, timer)


@router.post("/instance/{id}/state")
async def cancel_timer(
        id: int,
        request: timer_schemas.StateRequest,
        username: Annotated[CurrentUser, Depends(get_current_user)]
        ):
    return timer_service.change_stere(id, request)


@router.get("/active", response_model=list[timer_schemas.TimerInstance])
async def get_active_timers(
        username: Annotated[CurrentUser, Depends(get_current_user)],
        page: int = 0,
        size: int = 20
        ):
    return timer_service.get_active(page, size)
