from ..db import user_hero_repo, skillset_repo, equipment_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException


def teach_hero(user_id: int, hero_id: int, item_id: int, db: Session):
    item = equipment_repo.get_item_entry(user_id, item_id, db)
    if not item or item.amount < 1:
        raise no_item_exception()
    if not item.item.skill:
        raise no_skill_item_exception()
    hero = user_hero_repo.get_hero(user_id, hero_id, db)
    if not hero:
        raise no_such_hero_exception()
    skill = skillset_repo.get_skill(item.item.id, db)
    if not skill:
        raise not_initialized_exception()
    skillset_repo.teach_skill(hero.id, None, db)
    db.commit()
    return hero


def no_skill_item_exception():
    return HTTPException(
        status_code=400,
        detail="Cannot learn skill from this item!",
    )


def no_item_exception():
    return HTTPException(
        status_code=400,
        detail="No item in inventory!",
    )


def no_such_hero_exception():
    return HTTPException(
        status_code=404,
        detail="Not such hero!",
    )


def not_initialized_exception():
    return HTTPException(
        status_code=500,
        detail="Heroes not initialized",
    )
