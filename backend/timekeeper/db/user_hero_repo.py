from .models import UserHero
from sqlalchemy.orm import Session
from sqlalchemy import and_


def create_entry(hero_id, amount, user_id, db: Session):
    entry = UserHero(
            hero_id=hero_id,
            amount=amount,
            owner_id=user_id
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
