from ..db import item_repo, timer_repo, equipment_repo
from sqlalchemy.orm import Session


def get_reward(timer_id: int, user_id: int, db: Session):
    timer = timer_repo.get_timer_inst(timer_id, user_id, db)
    if not timer.reward_time:
        return
    item = item_repo.get_random_item(db)
    if not item:
        return
    equipment_repo.create_entry(item.id, 1, user_id, db)
    return item
