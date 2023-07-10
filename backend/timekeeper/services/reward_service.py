from ..db import item_repo
from sqlalchemy.orm import Session


def get_reward(timer_id: int, user_id: int, db: Session):
    return item_repo.get_random_item(db)
