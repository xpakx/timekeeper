from .manager import get_db
from ..routers.dto.timer_schemas import TimerRequest
from .models import Timer


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
