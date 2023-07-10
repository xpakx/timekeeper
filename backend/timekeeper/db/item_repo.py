from .models import Item
from sqlalchemy.orm import Session
import random


def get_random_item(db: Session):
    rnd = random.randint(1, 21)
    return db\
        .query(Item)\
        .where(
              Item.num == rnd
            )\
        .first()
