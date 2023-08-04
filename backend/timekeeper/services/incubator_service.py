from ..db import equipment_repo, incubator_repo, user_hero_repo, point_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException

INCUBATOR = 7


def install_incubator(user_id: int, db: Session):
    if not equipment_repo.subtract_items(INCUBATOR, 1, user_id, db):
        raise not_incubators_exception()
    if incubator_repo.get_installed(user_id, db) > 5:
        raise too_many_incubators_exceotion()
    incubator = incubator_repo.install_incubator(INCUBATOR, user_id, db)
    db.commit()
    return incubator


def get_incubators(user_id: int, db: Session):
    incubator_repo.get_incubators(user_id, db)


def insert_hero(user_id: int, hero_id: int, incubator_id: int, db: Session):
    hero = user_hero_repo.get_hero(user_id, hero_id, db)
    if not hero:
        raise no_such_hero_exception()
    if hero.incubated:
        raise hero_not_available_exception()
    incubator = incubator_repo.get_incubator(user_id, incubator_id, db)
    if not incubator:
        raise no_such_incubator_exception()
    if incubator.hero is not None:
        raise incubator_full_exception()
    points = point_repo.get_points(user_id, db)
    hero.incubated = True
    incubator.hero_id = hero.id
    incubator.initial_points = points.points if points else 0
    db.commit()


def get_hero(user_id: int, incubator_id: int, db: Session):
    pass


def delete_incubator(user_id: int, incubator_id: int, db: Session):
    pass


def not_incubators_exception():
    return HTTPException(
        status_code=400,
        detail="No incubators!",
    )


def too_many_incubators_exceotion():
    return HTTPException(
        status_code=400,
        detail="Too many incubators!",
    )


def no_such_hero_exception():
    return HTTPException(
        status_code=404,
        detail="No hero found",
    )


def no_such_incubator_exception():
    return HTTPException(
        status_code=404,
        detail="No incubator found",
    )


def incubator_full_exception():
    return HTTPException(
        status_code=400,
        detail="Incubator is full!",
    )


def hero_not_available_exception():
    return HTTPException(
        status_code=400,
        detail="Hero unavailable!",
    )
