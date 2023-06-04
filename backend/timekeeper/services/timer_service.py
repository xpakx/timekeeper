from ..routers.dto import timer_schemas
from ..db import timer_repo
from ..db.models import TimerState, TimerInstance
from sqlalchemy.orm import Session


def add_timer(request: timer_schemas.TimerRequest, user_id: int, db: Session):
    return timer_repo.create_timer(request, user_id, db)


def get_timers(page, size, user_id: int, db: Session):
    return timer_repo.get_timers(page, size, user_id, db)


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
    if request.state == TimerState.finished:
        timer_repo.finish_timer(timer_id, user_id, db)
    elif request.state == TimerState.cancelled:
        timer_repo.cancel_timer(timer_id, user_id, db)
    elif request.state == TimerState.failed:
        timer_repo.fail_timer(timer_id, user_id, db)


def get_active(page: int, size: int, user_id: int, db: Session):
    return timer_repo.get_active_timers(page, size, user_id, db)


def delete_timer(timer_id: int, user_id: int, db: Session):
    return timer_repo.delete_timer(timer_id, user_id, db)
