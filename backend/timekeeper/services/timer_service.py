from ..routers.dto import timer_request


def add_timer(request: timer_request.TimerRequest):
    print("adding")


def get_timers():
    print("fetching all requests")
