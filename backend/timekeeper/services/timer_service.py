from ..routers.dto import timer_schemas
from ..db import timer_repo


def add_timer(request: timer_schemas.TimerRequest):
    return timer_repo.create_timer(request)


def get_timers(page, size):
    return timer_repo.get_timers(page, size)


def edit_timer(timer_id: int, request: timer_schemas.TimerRequest):
    return timer_repo.edit_timer(timer_id, request)


def start_timer(timer_id: int):
    return timer_repo.start_timer(timer_id)
