from ..db import (
        hero_repo,
        user_hero_repo,
        battle_repo,
        team_repo,
        equipment_repo)
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from ..db.models import Battle, ItemType, UserHero, HeroMods, Team
from ..routers.dto.battle_schemas import MoveRequest, MoveType
from .mechanics import battle_mech_service as battle_mech


def create_battle(user_id: int, equipment_id: int, db: Session):
    team = team_repo.get_team(user_id, db)
    entry = equipment_repo.get_item_entry(equipment_id, user_id, db)
    old_battle = battle_repo.get_current_battle(user_id, db)
    if old_battle:
        raise already_in_battle_exception()
    if not entry:
        raise not_battle_ticket_exception()
    if not entry.item.item_type == ItemType.battle_ticket:
        raise not_battle_ticket_exception()
    if not entry or entry.amount < 1:
        raise no_battle_tickets_exception()
    entry.amount = entry.amount - 1
    if not team:
        raise team_not_initialized_exception()
    hero = team.hero_1
    if not hero:
        raise empty_team_exception()
    enemy = hero_repo.get_random_hero(db)
    if not enemy:
        raise not_initialized_exception()
    enemy_entry = user_hero_repo.create_entry(enemy.id, None, db)
    battle = battle_repo.create_entry(hero.id, enemy_entry, 1, user_id, db)
    db.commit()
    return battle


def select_first_hero_in_team(team: Team) -> UserHero:
    heroes = [
            team.hero_1,
            team.hero_2,
            team.hero_3,
            team.hero_4,
            team.hero_5,
            team.hero_6
            ]
    for hero in heroes:
        if hero is None:
            return None
        if hero.fainted:
            return None
        return hero
    return None


def get_battle(user_id: int, battle_id: int, db: Session) -> Optional[Battle]:
    battle = battle_repo.get_battle(user_id, battle_id, db)
    if not battle:
        raise not_battle_found_exception()
    return battle


def get_current_battle(user_id: int, db: Session) -> Optional[Battle]:
    return battle_repo.get_current_battle(user_id, db)


def not_initialized_exception():
    return HTTPException(
        status_code=500,
        detail="Heroes not initialized",
    )


def team_not_initialized_exception():
    return HTTPException(
        status_code=500,
        detail="Team not initialized",
    )


def not_such_hero_exception():
    return HTTPException(
        status_code=400,
        detail="Not such hero!",
    )


def empty_team_exception():
    return HTTPException(
        status_code=400,
        detail="Team is empty!",
    )


def not_battle_ticket_exception():
    return HTTPException(
        status_code=400,
        detail="No battle ticket!",
    )


def no_battle_tickets_exception():
    return HTTPException(
        status_code=400,
        detail="Not enough battle tickets!",
    )


def already_in_battle_exception():
    return HTTPException(
        status_code=400,
        detail="Already in battle!",
    )


def not_battle_found_exception():
    return HTTPException(
        status_code=404,
        detail="Battle not found!",
    )


def make_move(user_id: int, battle_id: int, move: MoveRequest, db: Session):
    battle: Battle = battle_repo.get_battle(user_id, battle_id, db)
    hero: UserHero = battle.hero
    hero_mods: HeroMods = battle.hero_mods
    enemy: UserHero = battle.enemy
    enemy_mods: HeroMods = battle.enemy_mods
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
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            enemy_skill,
            flee,
            switch)
    if player_first:
        player_hit = battle_mech.test_accuracy(
                hero,
                hero_mods,
                skill,
                enemy,
                enemy_mods)
        if player_hit:
            apply_damage(
                    hero,
                    hero_mods,
                    skill,
                    enemy,
                    enemy_mods)
        enemy_hit = battle_mech.test_accuracy(
                enemy,
                enemy_mods,
                enemy_skill,
                hero,
                hero_mods)
        if enemy_hit and battle_mech.calculate_hp(enemy) > enemy.damage:
            apply_damage(
                    enemy,
                    enemy_mods,
                    enemy_skill,
                    hero,
                    hero_mods)
    else:
        enemy_hit = battle_mech.test_accuracy(
                enemy,
                enemy_mods,
                enemy_skill,
                hero,
                hero_mods)
        if enemy_hit:
            apply_damage(
                    enemy,
                    enemy_mods,
                    enemy_skill,
                    hero,
                    hero_mods)
        player_hit = battle_mech.test_accuracy(
                hero,
                hero_mods,
                skill,
                enemy,
                enemy_mods)
        if player_hit and battle_mech.calculate_hp(hero) > hero.damage:
            apply_damage(
                    hero,
                    hero_mods,
                    skill,
                    enemy,
                    enemy_mods)
    battle.turn = battle.turn + 1
    db.commit()


def apply_damage(
        hero,
        hero_mods,
        skill,
        other_hero,
        other_mods):
    crit = battle_mech.test_crit(0)  # TODO: crit mod
    dmg = battle_mech.calculate_damage(
            hero,
            hero_mods,
            skill,
            other_hero,
            other_mods,
            crit)
    other_hero.damage = other_hero.damage + dmg
