from ..db import item_repo, timer_repo, equipment_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_reward(timer_id: int, user_id: int, db: Session):
    timer = timer_repo.get_timer_inst(timer_id, user_id, db)
    if timer.reward_time is None:
        raise not_reward_time_exception()
    if timer.rewarded:
        raise already_rewarded_exception()
    item = item_repo.get_random_item(db)
    if not item:
        raise not_initialized_exception()
    equipment_repo.create_entry(item.id, 1, user_id, db)
    timer.rewarded = True
    db.commit()
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


def already_rewarded_exception():
    return HTTPException(
        status_code=403,
        detail="Cannot reward twice",
    )


def get_items(page, size, user_id: int, db: Session):
    return equipment_repo.get_items(page, size, user_id, db)
