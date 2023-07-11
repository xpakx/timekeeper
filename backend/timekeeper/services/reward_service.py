from ..db import item_repo, timer_repo, equipment_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_reward(timer_id: int, user_id: int, db: Session):
    timer = timer_repo.get_timer_inst(timer_id, user_id, db)
    if not timer.reward_time:
        raise not_reward_time_exception()
    item = item_repo.get_random_item(db)
    if not item:
        raise not_initialized_exception()
    equipment_repo.create_entry(item.id, 1, user_id, db)
    return item


def not_initialized_exception():
    return HTTPException(
        status_code=500,
        detail="Rewards not initialized",
    )


def not_reward_time_exception():
    return HTTPException(
        status_code=400,
        detail="Cannot get reward from this timer",
    )
