from .manager import get_db
from ..routers.dto.timer_schemas import TimerRequest
from .models import Timer, TimerInstance, TimerState
import datetime
from fastapi import status, HTTPException


def create_timer(timer: TimerRequest, user_id: int):
    db = next(get_db())
    new_timer = Timer(
            name=timer.name,
            description=timer.description,
            duration_s=timer.duration_s,
            deleted=False,
            user_id=user_id
            )
    db.add(new_timer)
    db.commit()
    db.refresh(new_timer)
    return new_timer


def get_timers(page: int, size: int, user_id: int):
    offset = page*size
    db = next(get_db())
    return db.query(Timer).where(Timer.user_id == user_id).offset(offset).limit(size).all()


def edit_timer(timer_id: int, timer: TimerRequest, user_id: int):
    db = next(get_db())
    db_timer = db.get(Timer, timer_id)
    if db_timer:
        if db_timer.user_id != user_id:
            raise ownership_exception()
        db_timer.name = timer.name
        db_timer.description = timer.description
        db_timer.duration_s = timer.duration_s
        db.commit()
        db.refresh(db_timer)
    return db_timer


def start_timer(timer_id: int, user_id: int) -> TimerInstance:
    db = next(get_db())
    ownership = db.query(Timer.query.where(Timer.id == timer_id and Timer.user_id == user_id).exists()).scalar()
    if not ownership:
        raise ownership_exception()
    timer_instance = TimerInstance(
            timer_id=timer_id,
            start=datetime.datetime.utcnow,
            state=TimerState.running,
            user_id=user_id
            )
    db.add(timer_instance)
    db.commit()
    db.refresh(timer_instance)
    return timer_instance


def change_timer_state(timer_id: int, timer_state: int, user_id: int) -> None:
    db = next(get_db())
    timer = db.get(TimerInstance, timer_id)
    if timer:
        if timer.user_id != user_id:
            raise ownership_exception()
        timer.state = timer_state
        db.commit()


def finish_timer(timer_id: int, user_id: int) -> None:
    change_timer_state(timer_id, TimerState.finished, user_id)


def cancel_timer(timer_id: int, user_id: int) -> None:
    change_timer_state(timer_id, TimerState.cancelled, user_id)


def fail_timer(timer_id: int, user_id: int) -> None:
    change_timer_state(timer_id, TimerState.failed), user_id


def get_active_timers(page: int, size: int, user_id: int):
    offset = page*size
    db = next(get_db())
    return db.query(TimerInstance).where(
            TimerInstance.state == TimerState.running and TimerInstance.user_id == user_id
            ).offset(offset).limit(size).all()


def ownership_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
