from ..db import user_hero_repo, skillset_repo, equipment_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models import ItemType, UserHero


def teach_hero(
        user_id: int,
        hero_id: int,
        item_id: int,
        num: int,
        db: Session) -> UserHero:
    item = equipment_repo.get_item_entry(item_id, user_id, db)
    if not item or item.amount < 1:
        raise no_item_exception()
    if item.item.item_type != ItemType.skill:
        raise no_skill_item_exception()
    hero = user_hero_repo.get_hero(user_id, hero_id, db)
    if not hero:
        raise no_such_hero_exception()
    skill = skillset_repo.get_skill(item.item.id, db)
    if not skill:
        raise not_initialized_exception()
    if not skillset_repo.test_skill(hero.id, skill.id, db):
        raise not_teachable_exception()
    item.amount = item.amount - 1
    skillset_repo.teach_skill(hero.id, skill.id, num, db)
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
        detail="Skills not initialized",
    )


def not_teachable_exception():
    return HTTPException(
        status_code=400,
        detail="Not teachable!",
    )
