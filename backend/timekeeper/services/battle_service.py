from ..db import hero_repo, user_hero_repo, battle_repo, team_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from ..db.models import Battle, Skill, UserHero, ExpGroup
import math


def create_battle(user_id: int, db: Session):
    team = team_repo.get_team(user_id, db)
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


def calculate_if_player_moves_first(
        hero: UserHero,
        skill: Skill,
        enemy: UserHero,
        enemy_skill: Skill,
        flee: bool = False,
        switch: bool = False) -> bool:
    if (switch):
        return True
    priority = 0 if flee else skill.priority
    if (priority > enemy_skill.priority):
        return True
    if (enemy_skill.priority > priority):
        return False
    speed = calculate_speed(hero)
    enemy_speed = calculate_speed(enemy)
    return speed >= enemy_speed


def calculate_stat(base: int, iv: int, effort: int, lvl: int) -> int:
    return math.floor((2 * base + iv + effort) * lvl/100 + 5)


def calculate_speed(hero: UserHero):
    return calculate_stat(
            hero.hero.base_speed,
            hero.speed,
            0,
            exp_to_level(hero.hero.exp_group, hero.experience))


def exp_to_level(group: ExpGroup, exp: int) -> int:
    for i in range(1, 100):
        if level_to_exp(group, i) <= exp:
            return i
    return 100


def level_to_exp(group: ExpGroup, lvl: int) -> int:
    if group == ExpGroup.slow:
        return math.floor((5*lvl*lvl*lvl)/4)
    if group == ExpGroup.medium_slow:
        return math.floor((6*lvl*lvl*lvl)/5 - 15*lvl*lvl + 100*lvl - 140)
    if group == ExpGroup.medium_fast:
        return lvl*lvl*lvl
    if group == ExpGroup.fast:
        return math.floor((4*lvl*lvl*lvl)/5)
