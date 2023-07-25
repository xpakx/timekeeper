from ..db import hero_repo, user_hero_repo, equipment_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException

CRYSTAL = 6


def get_hero(timer_id: int, user_id: int, db: Session):
    if not equipment_repo.subtract_items(CRYSTAL, 1, user_id, db):
        raise not_enough_crystal_exception()
    hero = hero_repo.get_random_hero(db)
    if not hero:
        raise not_initialized_exception()
    user_hero_repo.create_entry(hero.id, user_id, db)
    db.commit()
    return hero


def get_crystals(user_id: int, db: Session):
    return equipment_repo.get_crystals(user_id, db)


def not_initialized_exception():
    return HTTPException(
        status_code=500,
        detail="Heroes not initialized",
    )


def not_enough_crystal_exception():
    return HTTPException(
        status_code=400,
        detail="Not enought crystals!",
    )


def get_heroes(page, size, user_id: int, db: Session):
    return user_hero_repo.get_heroes(page, size, user_id, db)
