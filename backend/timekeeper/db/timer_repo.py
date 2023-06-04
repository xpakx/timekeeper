from ..routers.dto.timer_schemas import TimerRequest
from .models import Timer, TimerInstance, TimerState
import datetime
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from sqlalchemy import and_


def create_timer(timer: TimerRequest, user_id: int, db: Session):
    new_timer = Timer(
            name=timer.name,
            description=timer.description,
            duration_s=timer.duration_s,
            deleted=False,
            owner_id=user_id
            )
    db.add(new_timer)
    db.commit()
    db.refresh(new_timer)
    return new_timer


def get_timers(page: int, size: int, user_id: int, db: Session):
    offset = page*size
    return db\
            .query(Timer)\
            .where(
                    and_(Timer.owner_id == user_id, Timer.deleted == false())
                    )\
            .offset(offset)\
            .limit(size)\
            .all()


def edit_timer(timer_id: int, timer: TimerRequest, user_id: int, db: Session):
    db_timer = db.get(Timer, timer_id)
    if db_timer:
        if db_timer.owner_id != user_id:
            raise ownership_exception()
        db_timer.name = timer.name
        db_timer.description = timer.description
        db_timer.duration_s = timer.duration_s
        db.commit()
        db.refresh(db_timer)
    return db_timer


def start_timer(timer_id: int, user_id: int, db: Session) -> TimerInstance:
    ownership = db\
            .query(
                    db
                    .query(Timer)
                    .where(
                        and_(Timer.id == timer_id, Timer.owner_id == user_id)
                        )
                    .exists()
            )\
            .scalar()
    if not ownership:
        raise ownership_exception()
    timer_instance = TimerInstance(
            timer_id=timer_id,
            start_time=datetime.datetime.utcnow,
            state=TimerState.running,
            owner_id=user_id
            )
    db.add(timer_instance)
    db.commit()
    db.refresh(timer_instance)
    return timer_instance


def change_timer_state(
        timer_id: int,
        timer_state: int,
        user_id: int,
        db: Session) -> None:
    timer = db.get(TimerInstance, timer_id)
    if timer:
        if timer.owner_id != user_id:
            raise ownership_exception()
        timer.state = timer_state
        db.commit()


def finish_timer(timer_id: int, user_id: int, db: Session) -> None:
    change_timer_state(timer_id, TimerState.finished, user_id, db)


def cancel_timer(timer_id: int, user_id: int, db: Session) -> None:
    change_timer_state(timer_id, TimerState.cancelled, user_id, db)


def fail_timer(timer_id: int, user_id: int, db: Session) -> None:
    change_timer_state(timer_id, TimerState.failed, user_id, db)


def get_active_timers(page: int, size: int, user_id: int, db: Session):
    offset = page*size
    return db\
            .query(TimerInstance)\
            .where(
                    and_(TimerInstance.state == TimerState.running, TimerInstance.owner_id == user_id)
            )\
            .offset(offset)\
            .limit(size)\
            .all()


def ownership_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def delete_timer(timer_id: int, user_id: int, db: Session) -> Timer:
    db_timer = db.get(Timer, timer_id)
    if db_timer:
        if db_timer.owner_id != user_id:
            raise ownership_exception()
        db_timer.deleted = True
        db.commit()
        db.refresh(db_timer)
    return db_timer
