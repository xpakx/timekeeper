from ..db import hero_repo, user_hero_repo, battle_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from ..db.models import Battle


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
