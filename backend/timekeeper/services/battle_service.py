from ..db import (
        hero_repo,
        user_hero_repo,
        battle_repo,
        team_repo,
        equipment_repo)
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from ..db.models import (
        Battle,
        ItemType,
        UserHero,
        HeroMods,
        HeroType,
        Team,
        Skill,
        StatusEffect,
        StageEffect,
        MoveCategory)
from ..routers.dto.battle_schemas import MoveRequest, MoveType
from .mechanics import battle_mech_service as battle_mech
import math
import random
from enum import Enum


def create_battle(user_id: int, equipment_id: int, db: Session) -> Battle:
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


def select_first_hero_in_team(team: Team) -> Optional[UserHero]:
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


def get_battle(user_id: int, battle_id: int, db: Session) -> Battle:
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


def skillset_not_initialized_exception():
    return HTTPException(
        status_code=500,
        detail="Skillset not initialized",
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


def make_move(
        user_id: int,
        battle_id: int,
        move: MoveRequest,
        db: Session) -> Battle:
    battle: Battle = battle_repo.get_battle(user_id, battle_id, db)
    if not battle:
        raise not_battle_found_exception()
    hero: UserHero = battle.hero
    hero_mods: HeroMods = battle.hero_mods
    enemy: UserHero = battle.enemy
    enemy_mods: HeroMods = battle.enemy_mods
    if not hero.skillset or not enemy.skillset:
        raise skillset_not_initialized_exception()
    skill = None
    flee = move.move == MoveType.flee
    switch = False
    skill = get_current_skill(move, hero)
    enemy_skill = get_enemy_skill(enemy)
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
        battle_turn(hero, hero_mods, skill, enemy, enemy_mods, enemy_skill)
    else:
        battle_turn(enemy, enemy_mods, enemy_skill, hero, hero_mods, skill)
    battle.turn = battle.turn + 1
    db.commit()
    return battle


def apply_damage(
        hero: UserHero,
        hero_mods: HeroMods,
        skill: Skill,
        other_hero: UserHero,
        other_mods: HeroMods) -> None:
    crit_mod = skill.crit_mod if skill.crit_mod else 0
    crit = battle_mech.test_crit(crit_mod)
    dmg = battle_mech.calculate_damage(
            hero,
            hero_mods,
            skill,
            other_hero,
            other_mods,
            crit)
    if hero.burned and skill.move_category == MoveCategory.physical:
        dmg = math.floor(dmg/2)
    other_hero.damage = other_hero.damage + dmg
    if battle_mech.calculate_hp(other_hero) <= other_hero.damage:
        other_hero.fainted = True


def battle_turn(
        hero: UserHero,
        hero_mods: HeroMods,
        skill: Optional[Skill],
        other_hero: UserHero,
        other_mods: HeroMods,
        other_skill: Optional[Skill]) -> None:
    hero_turn(hero, hero_mods, skill, other_hero, other_mods)
    apply_post_movement_statuses(hero, hero_mods, skill, other_hero)
    if not other_hero.fainted:
        hero_turn(other_hero, other_mods, other_skill, hero, hero_mods)
        apply_post_movement_statuses(other_hero, other_mods, other_skill, hero)


def hero_turn(
        hero: UserHero,
        hero_mods,
        skill: Optional[Skill],
        other_hero: UserHero,
        other_mods: HeroMods) -> None:
    if not skill:
        return
    able = is_hero_able_to_move(hero)
    if not able:
        return
    if skill.self_targetted:
        apply_status_skill(hero, hero_mods, skill)
        return
    hit = battle_mech.test_accuracy(
            hero,
            hero_mods,
            skill,
            other_hero,
            other_mods)
    if not hit:
        return
    if skill.move_category != MoveCategory.status:
        apply_damage(
                hero,
                hero_mods,
                skill,
                other_hero,
                other_mods)
        if other_hero.frozen and skill.move_type == MoveType.fire:
            other_hero.frozen = False
        if skill.secondary_status_chance:
            rand = random.randint(0, 100)
            if rand < skill.secondary_status_chance:
                apply_status_change(hero, hero_mods, skill.status_effect)
    else:
        apply_status_skill(other_hero, other_mods, skill)


def get_current_skill(move: MoveRequest, hero: UserHero) -> Optional[Skill]:
    if move.move != MoveType.skill:
        return None
    if move.id == 1:
        return hero.skillset.skill_1
    elif move.id == 2:
        return hero.skillset.skill_2
    elif move.id == 3:
        return hero.skillset.skill_3
    elif move.id == 4:
        return hero.skillset.skill_4


# TODO
def get_enemy_skill(hero: UserHero) -> Optional[Skill]:
    return hero.skillset.skill_1


def apply_status_skill(
        hero: UserHero,
        hero_mods: HeroMods,
        skill: Skill) -> None:
    if skill.status_effect:
        apply_status_change(hero, hero_mods, skill.status_effect)
    if skill.stage_effect:
        apply_stage_change(hero_mods, skill.stage_change, skill.mod)
    if skill.secondary_stage_effect:
        apply_stage_change(
                hero_mods,
                skill.secondary_stage_change,
                skill.secondary_mod)


class StageChangeResult():
    stage: StageEffect
    change: int

    def __init__(self, stage, change):
        self.stage = stage
        self.change = change


def apply_stage_change(
        hero_mods: HeroMods,
        effect: StageEffect,
        value: int) -> StageChangeResult:
    old_value = get_stage_for_effect(hero_mods, effect)
    if effect == StageEffect.attack:
        hero_mods.attack = calculate_new_stage(hero_mods.attack, value)
    elif effect == StageEffect.accuracy:
        hero_mods.accuracy = calculate_new_stage(hero_mods.accuracy, value)
    elif effect == StageEffect.evasion:
        hero_mods.evasion = calculate_new_stage(hero_mods.evasion, value)
    elif effect == StageEffect.defense:
        hero_mods.defense = calculate_new_stage(hero_mods.defense, value)
    elif effect == StageEffect.special_attack:
        hero_mods.special_attack = calculate_new_stage(
                hero_mods.special_attack,
                value)
    elif effect == StageEffect.special_defense:
        hero_mods.special_defense = calculate_new_stage(
                hero_mods.special_defense,
                value)
    elif effect == StageEffect.speed:
        hero_mods.speed = calculate_new_stage(hero_mods.speed, value)
    new_value = get_stage_for_effect(hero_mods, effect)
    return StageChangeResult(effect, new_value - old_value)


def get_stage_for_effect(hero_mods: HeroMods, effect: StageEffect) -> int:
    if effect == StageEffect.attack:
        return hero_mods.attack
    elif effect == StageEffect.accuracy:
        return hero_mods.accuracy
    elif effect == StageEffect.evasion:
        return hero_mods.evasion
    elif effect == StageEffect.defense:
        return hero_mods.defense
    elif effect == StageEffect.special_attack:
        return hero_mods.special_attack
    elif effect == StageEffect.special_defense:
        return hero_mods.special_defense
    elif effect == StageEffect.speed:
        return hero_mods.speed
    return 0


def calculate_new_stage(old_value: int, mod: int) -> int:
    value = old_value + mod
    if value > 6:
        return 6
    if value < -6:
        return -6
    return value


class StatusChangeEffect(Enum):
    immune = 1
    success = 2
    already_present = 3


def test_if_hero_has_types(hero: UserHero, types: list[HeroType]) -> bool:
    htype = hero.hero.hero_type
    if htype in types:
        return True
    htype = hero.hero.secondary_hero_type
    if htype in types:
        return True
    return False


def apply_poison_status(hero: UserHero) -> StatusChangeEffect:
    if hero.poisoned:
        return StatusChangeEffect.already_present
    if test_if_hero_has_types(hero, [HeroType.poison, HeroType.steel]):
        return StatusChangeEffect.immune
    hero.poisoned = True
    return StatusChangeEffect.success


def apply_poison_damage(hero: UserHero) -> None:
    hp = battle_mech.calculate_hp(hero)
    damage = math.floor(hp/8)
    if damage == 0:
        damage = 1
    hero.damage = hero.damage + damage
    if hp <= hero.damage:
        hero.fainted = True


def apply_burn_status(hero: UserHero) -> StatusChangeEffect:
    if hero.burned:
        return StatusChangeEffect.already_present
    if test_if_hero_has_types(hero, [HeroType.fire]):
        return StatusChangeEffect.immune
    hero.burned = True
    return StatusChangeEffect.success


def apply_burn_damage(hero: UserHero) -> None:
    hp = battle_mech.calculate_hp(hero)
    damage = math.floor(hp/8)
    if damage == 0:
        damage = 1
    hero.damage = hero.damage + damage
    if hp <= hero.damage:
        hero.fainted = True


def apply_frozen_status(hero: UserHero) -> StatusChangeEffect:
    if hero.frozen:
        return StatusChangeEffect.already_present
    if test_if_hero_has_types(hero, [HeroType.ice]):
        return StatusChangeEffect.immune
    hero.frozen = True
    return StatusChangeEffect.success


def apply_leech_seed(hero: UserHero, other_hero: UserHero) -> None:
    hp = battle_mech.calculate_hp(hero)
    other_hp = battle_mech.calculate_hp(other_hero)
    damage = math.floor(other_hp/8)
    if damage == 0:
        damage = 1
    other_hero.damage = other_hero.damage + damage
    if damage > hero.damage:
        damage = hero.damage
    hero.damage = hero.damage - damage
    if hp <= other_hero.damage:
        other_hero.fainted = True


def apply_paralyzed_status(hero: UserHero) -> StatusChangeEffect:
    if hero.paralyzed:
        return StatusChangeEffect.already_present
    if test_if_hero_has_types(hero, [HeroType.electric]):
        return StatusChangeEffect.immune
    hero.paralyzed = True
    return StatusChangeEffect.success


def apply_frozen_changes(hero: UserHero, move: Skill) -> None:
    if move.move_type == MoveType.fire:
        hero.frozen = False
    rand = random.randint(0, 100)
    if rand < 20:
        hero.frozen = False


def apply_asleep_changes(hero: UserHero) -> None:
    hero.sleep_counter = hero.sleep_counter - 1
    if hero.sleep_counter == 0:
        hero.asleep = False


def apply_post_movement_statuses(
        hero: UserHero,
        hero_mods: HeroMods,
        move: Skill,
        other_hero: UserHero) -> None:
    if not hero.fainted and hero_mods.leech_seed:
        apply_leech_seed(other_hero, hero)
    if not hero.fainted and hero.poisoned:
        apply_poison_damage(hero)
    if not hero.fainted and hero.burned:
        apply_burn_damage(hero)
    if not hero.fainted and hero.frozen:
        apply_frozen_changes(hero, move)
    if not hero.fainted and hero.asleep:
        apply_asleep_changes(hero)


class StatusChangeResult():
    status: StatusEffect
    effect: StatusChangeEffect

    def __init__(self, status, effect):
        self.status = status
        self.effect = effect


def apply_status_change(
        hero: UserHero,
        hero_mods: HeroMods,
        status: StatusEffect) -> list[StatusChangeResult]:
    result = []
    if status == StatusEffect.poisoned:
        effect = apply_poison_status(hero)
        result.append(StatusChangeResult(StatusEffect.poisoned, effect))
    if status == StatusEffect.burn:
        effect = apply_burn_status(hero)
        result.append(StatusChangeResult(StatusEffect.burn, effect))
    if status == StatusEffect.paralyzed:
        effect = apply_paralyzed_status(hero)
        result.append(StatusChangeResult(StatusEffect.paralyzed, effect))
    if status == StatusEffect.leech_seed:
        hero_mods.leech_seed = True
        result.append(StatusChangeResult(
            StatusEffect.leech_seed,
            StatusChangeEffect.success))
    if status == StatusEffect.asleep:
        hero.sleep_counter = random.randint(1, 6)
        hero_mods.asleep = True
        result.append(StatusChangeResult
                      (StatusEffect.sleep,
                       StatusChangeEffect.success))
    if status == StatusEffect.frozen:
        effect = apply_frozen_status(hero)
        result.append(StatusChangeResult(StatusEffect.frozen, effect))
    return result


def is_hero_able_to_move(hero: UserHero) -> bool:
    if hero.paralyzed:
        rand = random.randint(0, 100)
        if rand < 25:
            return False
    if hero.frozen or hero.asleep:
        return False
    return True
