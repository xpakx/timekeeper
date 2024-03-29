from .models import UserHero
from sqlalchemy.orm import Session
from sqlalchemy import and_
import random
from typing import Optional


def create_entry(hero_id, user_id, db: Session) -> UserHero:
    entry = UserHero(
            hero_id=hero_id,
            owner_id=user_id,
            attack=random.randint(0, 32),
            defense=random.randint(0, 32),
            speed=random.randint(0, 32),
            special_attack=random.randint(0, 32),
            special_defense=random.randint(0, 32),
            hp=random.randint(0, 32),
            level=1,
            experience=0,
            incubated=False,
            in_team=False,
            fainted=False,
            poisoned=False,
            burned=False,
            paralyzed=False,
            asleep=False,
            frozen=False,
            damage=0
            )
    db.add(entry)
    return entry


def get_heroes(
        page: int,
        size: int,
        user_id: int,
        db: Session) -> list[UserHero]:
    offset = page*size
    return db\
        .query(UserHero)\
        .where(
                    and_(UserHero.owner_id == user_id)
                    )\
        .offset(offset)\
        .limit(size)\
        .all()


def get_hero(user_id: int, hero_id: int, db: Session) -> Optional[UserHero]:
    return db\
        .query(UserHero)\
        .where(
                    and_(
                        UserHero.owner_id == user_id,
                        UserHero.id == hero_id
                        )
                    )\
        .first()
