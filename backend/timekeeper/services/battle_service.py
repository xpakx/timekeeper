from ..db import hero_repo, user_hero_repo, battle_repo, team_repo, equipment_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from ..db.models import Battle, ItemType
from .mechanics import battle_mech_service as battle_mech


def create_battle(user_id: int, equipment_id: int, db: Session):
    team = team_repo.get_team(user_id, db)
    entry = equipment_repo.get_item_entry(equipment_id, user_id, db)
    if not entry.item.item_type == ItemType.battle_ticket:
        raise not_battle_ticket_exception()
    if not entry or entry.amount < 1:
        raise no_battle_tickets_exception()
    entry.amount = entry.amount - 1
    if not team:
        raise not_initialized_exception()
    hero = team.hero_1
    if not hero:
        raise not_such_hero_exception()
    enemy = hero_repo.get_random_hero(db)
    if not enemy:
        raise not_initialized_exception()
    user_hero_repo.create_entry(enemy.id, None, db)
    battle = battle_repo.create_entry(hero.id, enemy.id, 1, user_id, db)
    db.commit()
    return battle


def get_battle(user_id: int, battle_id: int, db: Session) -> Optional[Battle]:
    return battle_repo.get_battle(user_id, battle_id, db)


def get_current_battle(user_id: int, db: Session) -> Optional[Battle]:
    return battle_repo.get_current_battle(user_id, db)


def not_initialized_exception():
    return HTTPException(
        status_code=500,
        detail="Heroes not initialized",
    )


def not_such_hero_exception():
    return HTTPException(
        status_code=400,
        detail="Not such hero!",
    )


def not_battle_ticket_exception():
    return HTTPException(
        status_code=400,
        detail="Not battle ticket!",
    )


def no_battle_tickets_exception():
    return HTTPException(
        status_code=404,
        detail="Not enough battle tickets!",
    )
