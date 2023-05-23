from .manager import get_db
from ..routers.dto.timer_schemas import TimerRequest
from .models import Timer, TimerInstance, TimerState
import datetime


def create_timer(timer: TimerRequest):
    db = next(get_db())
    new_timer = Timer(
            name=timer.name,
            description=timer.description,
            duration_s=timer.duration_s
            )
    db.add(new_timer)
    db.commit()
    db.refresh(new_timer)
    return new_timer


def get_timers(page: int, size: int):
    offset = page*size
    db = next(get_db())
    return db.query(Timer).offset(offset).limit(size).all()


def edit_timer(timer_id: int, timer: TimerRequest):
    db = next(get_db())
    db_timer = db.get(Timer, timer_id)
    if db_timer:
        db_timer.name = timer.name
        db_timer.description = timer.description
        db_timer.duration_s = timer.duration_s
        db.commit()
        db.refresh(db_timer)
    return db_timer


def start_timer(timer_id: int) -> TimerInstance:
    db = next(get_db())
    timer_instance = TimerInstance(
            timer_id=timer_id,
            start=datetime.datetime.utcnow,
            state=TimerState.running
            )
    db.add(timer_instance)
    db.commit()
    db.refresh(timer_instance)
    return timer_instance


def change_timer_state(timer_id: int, timer_state: int) -> None:
    db = next(get_db())
    timer = db.get(TimerInstance, timer_id)
    if timer:
        timer.state = timer_state
        db.commit()


def finish_timer(timer_id: int) -> None:
    change_timer_state(timer_id, TimerState.finished)


def cancel_timer(timer_id: int) -> None:
    change_timer_state(timer_id, TimerState.cancelled)


def fail_timer(timer_id: int) -> None:
    change_timer_state(timer_id, TimerState.failed)
