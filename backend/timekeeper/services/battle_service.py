from ..db import (
        hero_repo,
        user_hero_repo,
        battle_repo,
        team_repo,
        equipment_repo)
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from ..db.models import Battle, ItemType, UserHero
from ..routers.dto.battle_schemas import MoveRequest, MoveType
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


def make_move(user_id: int, battle_id: int, move: MoveRequest, db: Session):
    battle: Battle = battle_repo.get_battle(user_id, battle_id, db)
    hero: UserHero = battle.hero
    enemy: UserHero = battle.enemy
    skill = None
    flee = move.move == MoveType.flee
    switch = False
    if move.move == MoveType.skill:
        if move.id == 1:
            skill = hero.skills.skill_1
        elif move.id == 2:
            skill = hero.skills.skill_2
        elif move.id == 3:
            skill = hero.skills.skill_3
        elif move.id == 4:
            skill = hero.skills.skill_4
    enemy_skill = enemy.skills.skill_1  # TODO
    player_first = battle_mech.calculate_if_player_moves_first(
            hero,
            skill,
            battle.hero_speed,
            enemy,
            enemy_skill,
            battle.enemy_speed,
            flee,
            switch)
    if player_first:
        player_hit = battle_mech.test_accuracy(
                hero,
                skill,
                enemy,
                battle.hero_accuracy,
                battle.enemy_evasion)
        if player_hit:
            apply_damage(
                    hero,
                    skill,
                    enemy,
                    battle.hero_attack,
                    battle.hero_special_attack,
                    battle.enemy_defense,
                    battle.enemy_special_defense)
        enemy_hit = battle_mech.test_accuracy(
                enemy,
                enemy_skill,
                hero,
                battle.enemy_accuracy,
                battle.hero_evasion)
        if enemy_hit and battle_mech.calculate_hp(enemy) > enemy.damage:
            apply_damage(
                    enemy,
                    enemy_skill,
                    hero,
                    battle.enemy_attack,
                    battle.enemy_special_attack,
                    battle.hero_defense,
                    battle.hero_special_defense)
    else:
        enemy_hit = battle_mech.test_accuracy(
                enemy,
                enemy_skill,
                hero,
                battle.enemy_accuracy,
                battle.hero_evasion)
        if enemy_hit:
            apply_damage(
                    enemy,
                    enemy_skill,
                    hero,
                    battle.enemy_attack,
                    battle.enemy_special_attack,
                    battle.hero_defense,
                    battle.hero_special_defense)
        player_hit = battle_mech.test_accuracy(
                hero,
                skill,
                enemy,
                battle.hero_accuracy,
                battle.hero_evasion)
        if player_hit and battle_mech.calculate_hp(hero) > hero.damage:
            apply_damage(
                    hero,
                    skill,
                    enemy,
                    battle.hero_attack,
                    battle.hero_special_attack,
                    battle.enemy_defense,
                    battle.enemy_special_defense)
    battle.turn = battle.turn + 1
    db.commit()


def apply_damage(
        hero,
        skill,
        other_hero,
        atk_stage,
        spec_atk_stage,
        def_stage,
        spec_def_stage):
    crit = battle_mech.test_crit(0)  # TODO: crit mod
    dmg = battle_mech.calculate_damage(
            hero,
            atk_stage,
            spec_atk_stage,
            skill,
            other_hero,
            def_stage,
            spec_def_stage,
            crit)
    other_hero.damage = other_hero.damage + dmg
