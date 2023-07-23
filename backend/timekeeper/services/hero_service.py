from ..db import hero_repo, user_hero_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_hero(timer_id: int, user_id: int, db: Session):
    hero = hero_repo.get_random_hero(db)
    if not hero:
        raise not_initialized_exception()
    user_hero_repo.create_entry(hero.id, user_id, db)
    db.commit()
    return hero


def not_initialized_exception():
    return HTTPException(
        status_code=500,
        detail="Heroes not initialized",
    )


def get_heroes(page, size, user_id: int, db: Session):
    return user_hero_repo.get_heroes(page, size, user_id, db)
