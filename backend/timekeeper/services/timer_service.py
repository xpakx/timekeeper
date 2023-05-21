from ..routers.dto import timer_schemas
from ..db import timer_repo


def add_timer(request: timer_schemas.TimerRequest):
    return timer_repo.create_timer(request)


def get_timers():
    return timer_repo.get_timers(0, 20)
