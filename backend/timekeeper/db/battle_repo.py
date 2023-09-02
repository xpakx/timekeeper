from .models import Battle
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from sqlalchemy.sql.expression import false


def create_entry(
        hero_id: int,
        enemy_id: int,
        enemies: int,
        user_id,
        db: Session):
    entry = Battle(
            hero_id=hero_id,
            enemy_id=enemy_id,
            owner_id=user_id,
            hero_accuracy=0,
            hero_evasion=0,
            enemy_accuracy=0,
            enemy_evasion=0,
            turn=1,
            enemies=enemies,
            finished=False
            )
    db.add(entry)
    return entry


def get_battle(user_id: int, battle_id: int, db: Session) -> Optional[Battle]:
    return db\
        .query(Battle)\
        .where(
                    and_(
                        Battle.owner_id == user_id,
                        Battle.id == battle_id
                        )
                    )\
        .first()


def get_current_battle(user_id: int, db: Session) -> Optional[Battle]:
    return db\
        .query(Battle)\
        .where(
                    and_(
                        Battle.owner_id == user_id,
                        Battle.finished == false()
                        )
                    )\
        .first()
