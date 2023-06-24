from ..routers.dto import timer_schemas
from ..db import timer_repo, point_repo
from ..db.models import TimerInstance, TimerState
from sqlalchemy.orm import Session
import random


def add_timer(request: timer_schemas.TimerRequest, user_id: int, db: Session):
    return timer_repo.create_timer(request, user_id, db)


def get_timers(page, size, user_id: int, db: Session):
    return timer_repo.get_timers(page, size, user_id, db)


def get_timer(timer_id: int,
              user_id: int,
              db: Session):
    return timer_repo.get_timer(timer_id, user_id, db)


def edit_timer(timer_id: int,
               request: timer_schemas.TimerRequest,
               user_id: int,
               db: Session):
    return timer_repo.edit_timer(timer_id, request, user_id, db)


def start_timer(timer_id: int, user_id: int, db: Session) -> TimerInstance:
    return timer_repo.start_timer(timer_id, user_id, db)


def change_state(timer_id: int,
                 request: timer_schemas.StateRequest,
                 user_id: int,
                 db: Session) -> None:
    timer = timer_repo.change_timer_state(timer_id, request.state, user_id, db)
    if timer.rewarded and request.state == TimerState.finished:
        reward = random.randint(1, 5)
        point_repo.add_points(reward, user_id, db)


def get_active(page: int, size: int, user_id: int, db: Session):
    return timer_repo.get_active_timers(page, size, user_id, db)


def delete_timer(timer_id: int, user_id: int, db: Session):
    return timer_repo.delete_timer(timer_id, user_id, db)


def get_history(page: int, size: int, user_id: int, db: Session):
    return timer_repo.get_history(page, size, user_id, db)


def get_timer_history(page: int, size: int, user_id: int, timer_id: int, db: Session):
    return timer_repo.get_timer_history(page, size, user_id, timer_id, db)
