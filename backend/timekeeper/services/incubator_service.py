from ..db import equipment_repo, incubator_repo
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
    pass


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
