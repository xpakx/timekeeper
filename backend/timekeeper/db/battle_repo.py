from .models import Battle, HeroMods
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
    hero = HeroMods(
            accuracy=0,
            evasion=0,
            accuracy=0,
            attack=0,
            defense=0,
            special_attack=0,
            special_defense=0,
            speed=0)
    enemy = HeroMods(
            accuracy=0,
            evasion=0,
            accuracy=0,
            attack=0,
            defense=0,
            special_attack=0,
            special_defense=0,
            speed=0)
    entry = Battle(
            hero_id=hero_id,
            hero_mods=hero,
            enemy_id=enemy_id,
            enemy_mods=enemy,
            owner_id=user_id,
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
