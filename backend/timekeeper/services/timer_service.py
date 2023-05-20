from ..routers.dto import timer_request
from ..db import timer_repo


def add_timer(request: timer_request.TimerRequest):
    return timer_repo.create_timer(request)


def get_timers():
    add_timer({"name": "aaa", "description": "desc", "duration_s": 60})
    print("fetching all requests")
