from .models import Item
from sqlalchemy.orm import Session
import random

COMMON = range(1, 6)
UNCOMMON = range(6, 16)
RARE = range(16, 21)


def get_random_item(db: Session):
    rnd = random.randint(0, 6)
    if rnd < 3:
        rnd = random.choice(COMMON)
    elif rnd < 5:
        rnd = random.choice(UNCOMMON)
    else:
        rnd = random.choice(RARE)

    return db\
        .query(Item)\
        .where(
              Item.num == rnd
            )\
        .first()
