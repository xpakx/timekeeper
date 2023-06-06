from fastapi import APIRouter, Depends, Query
from .dto import timer_schemas
from ..services import timer_service
from typing import Annotated
from ..security.jwt import get_current_user, CurrentUser
from ..db.manager import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/timers")


@router.post("/", response_model=timer_schemas.TimerResponse)
async def add_timer(
        timer: timer_schemas.TimerRequest,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return timer_service.add_timer(timer, user.id, db)


@router.get("/", response_model=list[timer_schemas.TimerResponse])
async def get_timers(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        page: Annotated[int, Query(ge=0)] = 0,
        size: Annotated[int, Query(ge=1, le=20)] = 20,
        db: Session = Depends(get_db)
        ):
    return timer_service.get_timers(page, size, user.id, db)


@router.put("/{id}", response_model=timer_schemas.TimerResponse)
async def edit_timer(
        id: int,
        timer: timer_schemas.TimerRequest,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return timer_service.edit_timer(id, timer, user.id, db)


@router.post("/instances/{id}/state")
async def change_timer_state(
        id: int,
        request: timer_schemas.StateRequest,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return timer_service.change_state(id, request, user.id, db)


@router.get("/active", response_model=list[timer_schemas.TimerInstance])
async def get_active_timers(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        page: Annotated[int, Query(ge=0)] = 0,
        size: Annotated[int, Query(ge=1, le=20)] = 20,
        db: Session = Depends(get_db)
        ):
    return timer_service.get_active(page, size, user.id, db)


@router.delete("/{id}", response_model=timer_schemas.TimerResponse)
async def delete_timer(id: int,
                       user: Annotated[CurrentUser, Depends(get_current_user)],
                       db: Session = Depends(get_db)
                       ):
    return timer_service.delete_timer(id, user.id, db)


@router.post("/{id}/instances", response_model=timer_schemas.TimerInstance)
async def start_timer(id: int,
                      user: Annotated[CurrentUser, Depends(get_current_user)],
                      db: Session = Depends(get_db)
                      ):
    return timer_service.start_timer(id, user.id, db)
