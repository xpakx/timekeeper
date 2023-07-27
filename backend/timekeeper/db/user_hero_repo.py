from .models import UserHero
from sqlalchemy.orm import Session
from sqlalchemy import and_
import random


def create_entry(hero_id, user_id, db: Session):
    entry = UserHero(
            hero_id=hero_id,
            owner_id=user_id,
            attack=random.randint(0, 16),
            defense=random.randint(0, 16),
            speed=random.randint(0, 16),
            special=random.randint(0, 16)
            )
    db.add(entry)


def get_heroes(page: int, size: int, user_id: int, db: Session):
    offset = page*size
    return db\
        .query(UserHero)\
        .where(
                    and_(UserHero.owner_id == user_id)
                    )\
        .offset(offset)\
        .limit(size)\
        .all()
