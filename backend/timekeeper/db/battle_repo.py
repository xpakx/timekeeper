from .models import Battle, HeroMods, UserHero
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from sqlalchemy.sql.expression import false


def create_entry(
        hero_id: int,
        enemy: UserHero,
        enemies: int,
        user_id,
        db: Session) -> Battle:
    hero = HeroMods(
            accuracy=0,
            evasion=0,
            attack=0,
            defense=0,
            special_attack=0,
            special_defense=0,
            speed=0,
            flee_attempts=0,
            leech_seed=False)
    enemy_mods = HeroMods(
            accuracy=0,
            evasion=0,
            attack=0,
            defense=0,
            special_attack=0,
            special_defense=0,
            speed=0,
            flee_attempts=0,
            leech_seed=False)
    entry = Battle(
            hero_id=hero_id,
            hero_mods=hero,
            enemy=enemy,
            enemy_mods=enemy_mods,
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


def in_battle(user_id: int, db: Session) -> bool:
    entry = db\
        .query(Battle)\
        .where(
                    and_(
                        Battle.owner_id == user_id,
                        Battle.finished == false()
                        )
                    )\
        .first()
    if entry:
        return True
    else:
        return False
