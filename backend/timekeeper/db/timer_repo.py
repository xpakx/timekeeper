from ..routers.dto.timer_schemas import TimerRequest
from .models import Timer, TimerInstance, TimerState, TimerDifficulty
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from sqlalchemy import and_
from sqlalchemy.sql import func
import random
from typing import Optional
import datetime


def create_timer(timer: TimerRequest, user_id: int, db: Session) -> Timer:
    new_timer = Timer(
            name=timer.name,
            description=timer.description,
            duration_s=timer.duration_s,
            deleted=False,
            rewarded=timer.rewarded if timer.rewarded is not None else False,
            difficulty=timer.difficulty,
            owner_id=user_id,
            autofinish=timer.autofinish if timer.autofinish is not None else False
            )
    db.add(new_timer)
    db.commit()
    db.refresh(new_timer)
    return new_timer


def get_timers(page: int, size: int, user_id: int, db: Session) -> list[Timer]:
    offset = page*size
    return db\
        .query(Timer)\
        .where(
                    and_(Timer.owner_id == user_id, Timer.deleted == false())
                    )\
        .offset(offset)\
        .limit(size)\
        .all()


def get_timer(timer_id: int, user_id: int, db: Session) -> Timer:
    db_timer = db.get(Timer, timer_id)
    if (not db_timer) or db_timer.owner_id != user_id:
        raise not_found_exception()
    return db_timer


def edit_timer(
        timer_id: int,
        timer: TimerRequest,
        user_id: int,
        db: Session) -> Timer:
    db_timer = db.get(Timer, timer_id)
    if db_timer:
        if db_timer.owner_id != user_id:
            raise ownership_exception()
        db_timer.name = timer.name
        db_timer.description = timer.description
        db_timer.duration_s = timer.duration_s
        if timer.autofinish is not None:
            db_timer.autofinish = timer.autofinish
        if timer.rewarded is not None:
            db_timer.rewarded = timer.rewarded
        if timer.difficulty is not None:
            db_timer.difficulty = timer.difficulty
        db.commit()
        db.refresh(db_timer)
    return db_timer


def start_timer(timer_id: int, user_id: int, db: Session) -> TimerInstance:
    db_timer = db.get(Timer, timer_id)
    if not db_timer or db_timer.owner_id != user_id:
        raise ownership_exception()
    reward = db_timer.rewarded and randomize_reward_generation(db_timer.difficulty)
    timer_instance = TimerInstance(
            timer_id=timer_id,
            start_time=func.now(),
            state=TimerState.running,
            reward_time=(random.randint(0, db_timer.duration_s) * 1000) if reward else None,
            rewarded=False,
            owner_id=user_id
            )
    db.add(timer_instance)
    db.commit()
    db.refresh(timer_instance)
    return timer_instance


def randomize_reward_generation(difficulty: Optional[TimerDifficulty]) -> bool:
    if not difficulty or difficulty == TimerDifficulty.trivial:
        return random.randint(0, 5) > 3
    if difficulty == TimerDifficulty.easy:
        return random.randint(0, 4) > 2
    if difficulty == TimerDifficulty.medium:
        return random.randint(0, 3) > 1
    if difficulty == TimerDifficulty.hard:
        return random.randint(0, 2) > 0
    return False


def change_timer_state(
        timer_id: int,
        timer_state: TimerState,
        user_id: int,
        db: Session) -> None:
    timer: TimerInstance = db.get(TimerInstance, timer_id)
    if timer:
        if timer.owner_id != user_id:
            raise ownership_exception()
        if timer_state == TimerState.finished:
            now = datetime.datetime.now(timer.start_time.astimezone().tzinfo)
            diff = now - timer.start_time
            if diff.total_seconds() < timer.timer.duration_s:
                raise timer_not_finished_exception()
        timer.state = timer_state
        if timer_state != TimerState.running:
            timer.end_time = func.now()
        db.commit()
        return timer.timer
    else:
        raise ownership_exception()


def get_active_timers(
        page: int,
        size: int,
        user_id: int,
        db: Session) -> list[TimerInstance]:
    offset = page*size
    return db\
        .query(TimerInstance)\
        .where(
             and_(
                 TimerInstance.state == TimerState.running,
                 TimerInstance.owner_id == user_id)
            )\
        .offset(offset)\
        .limit(size)\
        .all()


def ownership_exception():
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not an owner of this timer",
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


def not_found_exception():
    return HTTPException(
        status_code=404,
        detail="Timer not found",
    )


def get_history(
        page: int,
        size: int,
        user_id: int,
        db: Session) -> list[TimerInstance]:
    offset = page*size
    return db\
        .query(TimerInstance)\
        .where(
             and_(
                 TimerInstance.state != TimerState.running,
                 TimerInstance.owner_id == user_id)
            )\
        .order_by(TimerInstance.end_time.desc())\
        .offset(offset)\
        .limit(size)\
        .all()


def get_timer_history(
        page: int,
        size: int,
        user_id: int,
        timer_id: int,
        db: Session) -> list[TimerInstance]:
    offset = page*size
    return db\
        .query(TimerInstance)\
        .where(
             and_(
                 TimerInstance.state != TimerState.running,
                 TimerInstance.owner_id == user_id,
                 TimerInstance.timer_id == timer_id)
            )\
        .order_by(TimerInstance.end_time.desc())\
        .offset(offset)\
        .limit(size)\
        .all()


def get_timer_inst(timer_id: int, user_id: int, db: Session) -> TimerInstance:
    db_timer = db.get(TimerInstance, timer_id)
    if (not db_timer) or db_timer.owner_id != user_id:
        raise not_found_exception()
    return db_timer


def timer_not_finished_exception():
    return HTTPException(
        status_code=400,
        detail="Timer cannot be finished at this moment!",
    )
