from ..routers.dto import timer_schemas
from ..db import timer_repo
from ..db.models import TimerState


def add_timer(request: timer_schemas.TimerRequest):
    return timer_repo.create_timer(request)


def get_timers(page, size):
    return timer_repo.get_timers(page, size)


def edit_timer(timer_id: int, request: timer_schemas.TimerRequest):
    return timer_repo.edit_timer(timer_id, request)


def start_timer(timer_id: int):
    return timer_repo.start_timer(timer_id)


def finish_timer(timer_id: int, request: timer_schemas.StateRequest) -> None:
    if request.state == TimerState.finished:
        timer_repo.finish_timer(timer_id)
    elif request.state == TimerState.cancelled:
        timer_repo.cancel_timer(timer_id)
    elif request.state == TimerState.failed:
        timer_repo.fail_timer(timer_id)


def get_active(page: int, size: int):
    return timer_repo.get_active_timers(page, size)
