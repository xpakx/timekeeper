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
        MoveCategory,
        EquipmentEntry,
        Item)
from .model.battle_model import (
        StatusChangeEffect,
        StatusChangeResult,
        StageChangeResult,
        StatusSkillResults,
        DamageSkillResults,
        SkillResult,
        MoveResult,
        MovementTestResult,
        BattleResult,
        PostTurnEffects,
        PostTurnResult)
from ..routers.dto.battle_schemas import MoveRequest, MoveType
from .mechanics import battle_mech_service as battle_mech
import math
import random


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
    enemy = hero_repo.get_random_hero_for_encounter(db, entry.item.id)
    if not enemy:
        # TODO temporary fallback for tests, delete it later
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
        db: Session) -> BattleResult:
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
    item = get_item(move, user_id, db)
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
    turn = None
    if player_first:
        turn = battle_turn(
                hero,
                hero_mods,
                skill,
                enemy,
                enemy_mods,
                enemy_skill,
                flee,
                False,
                item,
                None)
    else:
        turn = battle_turn(
                enemy,
                enemy_mods,
                enemy_skill,
                hero,
                hero_mods,
                skill,
                False,
                flee,
                None,
                item)
    battle.turn = battle.turn + 1
    if enemy.fainted:
        battle.finished = True
    if turn.first_fled or turn.second_fled or turn.catched:
        battle.finished = True
    db.commit()
    hero_hp = battle_mech.calculate_hp(hero)
    enemy_hp = battle_mech.calculate_hp(enemy)
    result = BattleResult(
            turn=turn,
            hero_first=player_first,
            hero_hp=hero_hp,
            enemy_hp=enemy_hp)
    return result


def apply_damage(
        hero: UserHero,
        hero_mods: HeroMods,
        skill: Skill,
        other_hero: UserHero,
        other_mods: HeroMods) -> DamageSkillResults:
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
    other_hero_hp = battle_mech.calculate_hp(other_hero)
    if other_hero_hp <= other_hero.damage:
        other_hero.fainted = True
    result = DamageSkillResults()
    result.critical = crit
    result.new_hp = other_hero_hp - other_hero.damage
    result.effectiveness = battle_mech.get_effectiveness(
            skill.move_type,
            other_hero.hero)
    return result


def battle_turn(
        hero: UserHero,
        hero_mods: HeroMods,
        skill: Optional[Skill],
        other_hero: UserHero,
        other_mods: HeroMods,
        other_skill: Optional[Skill],
        flee: bool,
        other_flee: bool,
        item: Optional[Item],
        other_item: Optional[Item]) -> MoveResult:
    if flee and test_flee(hero, hero_mods, other_hero, other_mods):
        return MoveResult(first_fled=True)
    catched = None
    if item and item.item_type == ItemType.pokeball:
        catched = battle_mech.test_catching(other_hero, other_mods, 1)
        if catched:
            return MoveResult(catched=True)
    first = hero_turn(hero, hero_mods, skill, other_hero, other_mods)
    first_changes = apply_post_movement_statuses(hero, hero_mods, skill, other_hero)
    if catched is not None:
        return MoveResult(catched=catched, first=first, first_changes=first_changes)
    if other_hero.fainted:
        return MoveResult(first=first, first_changes=first_changes)
    if other_flee and test_flee(other_hero, other_mods, hero, hero_mods):
        return MoveResult(second_fled=True, first=first, first_changes=first_changes)
    if other_item and other_item.item_type == ItemType.pokeball:
        catched = battle_mech.test_catching(hero, hero_mods, 1)
        if catched:
            return MoveResult(catched=True, first=first, first_changes=first_changes)
    second = hero_turn(
            other_hero,
            other_mods,
            other_skill,
            hero,
            hero_mods)
    second_changes = apply_post_movement_statuses(other_hero, other_mods, other_skill, hero)
    result = MoveResult(
            first=first,
            first_changes=first_changes,
            second=second,
            second_changes=second_changes,
            catched=catched)
    return result


def test_flee(hero: UserHero, hero_mods: HeroMods, other_hero: UserHero, other_mods: HeroMods) -> bool:
    fled = battle_mech.test_fleeing(hero, hero_mods, other_hero, other_mods)
    hero_mods.flee_attempts = hero_mods.flee_attempts + 1
    return fled


def hero_turn(
        hero: UserHero,
        hero_mods,
        skill: Optional[Skill],
        other_hero: UserHero,
        other_mods: HeroMods) -> SkillResult:
    result = SkillResult()
    if not skill:
        return result
    result.name = skill.name
    result.able = is_hero_able_to_move(hero)
    if not result.able.able:
        return result
    if skill.self_targetted:
        change = apply_status_skill(hero, hero_mods, skill)
        result.status_skill = change
        result.self_targetted = True
        return result
    hit = battle_mech.test_accuracy(
            hero,
            hero_mods,
            skill,
            other_hero,
            other_mods)
    if not hit:
        result.missed = True
        return result
    if skill.move_category != MoveCategory.status:
        damage = apply_damage(
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
                change = apply_status_change(
                        hero,
                        hero_mods,
                        skill.status_effect)
                damage.secondary_status_changes = change
        result.skill = damage
    else:
        change = apply_status_skill(other_hero, other_mods, skill)
        result.status_skill = change
    result.fainted = hero.fainted
    result.second_fainted = other_hero.fainted
    return result


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
    skills: list[Skill] = [hero.skillset.skill_1,
                           hero.skillset.skill_2,
                           hero.skillset.skill_3,
                           hero.skillset.skill_4]
    best_skill: Skill = None
    for skill in skills:
        if not skill:
            continue
        if skill.move_category == MoveCategory.status:
            continue
        if not best_skill or skill.power > best_skill.power:
            best_skill = skill
    return best_skill


def apply_status_skill(
        hero: UserHero,
        hero_mods: HeroMods,
        skill: Skill) -> StatusSkillResults:
    result = StatusSkillResults()
    if skill.status_effect:
        change = apply_status_change(hero, hero_mods, skill.status_effect)
        result.append(change)
    if skill.stage_effect:
        change = apply_stage_change(hero_mods, skill.stage_change, skill.mod)
        result.append(change)
    if skill.secondary_stage_effect:
        change = apply_stage_change(
                hero_mods,
                skill.secondary_stage_change,
                skill.secondary_mod)
        result.append(change)


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
    return StageChangeResult(stage=effect, change=new_value - old_value)


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


def apply_poison_damage(hero: UserHero) -> PostTurnEffects:
    hp = battle_mech.calculate_hp(hero)
    damage = math.floor(hp/8)
    if damage == 0:
        damage = 1
    hero.damage = hero.damage + damage
    if hp <= hero.damage:
        hero.fainted = True
    hero_hp = battle_mech.calculate_hp(hero)
    new_hp = hero_hp - hero.damage
    return PostTurnEffects(reason=StatusEffect.poisoned, new_hp=new_hp)


def apply_burn_status(hero: UserHero) -> StatusChangeEffect:
    if hero.burned:
        return StatusChangeEffect.already_present
    if test_if_hero_has_types(hero, [HeroType.fire]):
        return StatusChangeEffect.immune
    hero.burned = True
    return StatusChangeEffect.success


def apply_burn_damage(hero: UserHero) -> PostTurnEffects:
    hp = battle_mech.calculate_hp(hero)
    damage = math.floor(hp/8)
    if damage == 0:
        damage = 1
    hero.damage = hero.damage + damage
    if hp <= hero.damage:
        hero.fainted = True
    return PostTurnEffects(reason=StatusEffect.burned, hp_change=damage)


def apply_frozen_status(hero: UserHero) -> StatusChangeEffect:
    if hero.frozen:
        return StatusChangeEffect.already_present
    if test_if_hero_has_types(hero, [HeroType.ice]):
        return StatusChangeEffect.immune
    hero.frozen = True
    return StatusChangeEffect.success


def apply_leech_seed(hero: UserHero, other_hero: UserHero) -> PostTurnEffects:
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
    return PostTurnEffects(reason=StatusEffect.leech_seed, hp_change=damage)


def apply_paralyzed_status(hero: UserHero) -> StatusChangeEffect:
    if hero.paralyzed:
        return StatusChangeEffect.already_present
    if test_if_hero_has_types(hero, [HeroType.electric]):
        return StatusChangeEffect.immune
    hero.paralyzed = True
    return StatusChangeEffect.success


def apply_frozen_changes(hero: UserHero, move: Skill) -> PostTurnEffects:
    if move.move_type == MoveType.fire:
        hero.frozen = False
    rand = random.randint(0, 100)
    if rand < 20:
        hero.frozen = False
    return PostTurnEffects(reason=StatusEffect.frozen, status_end=hero.frozen)


def apply_asleep_changes(hero: UserHero) -> None:
    hero.sleep_counter = hero.sleep_counter - 1
    if hero.sleep_counter == 0:
        hero.asleep = False
    return PostTurnEffects(reason=StatusEffect.asleep, status_end=hero.frozen)


def apply_post_movement_statuses(
        hero: UserHero,
        hero_mods: HeroMods,
        move: Skill,
        other_hero: UserHero) -> PostTurnResult:
    result = []
    if not hero.fainted and hero_mods.leech_seed:
        change = apply_leech_seed(other_hero, hero)
        result.append(change)
    if not hero.fainted and hero.poisoned:
        change = apply_poison_damage(hero)
        result.append(change)
    if not hero.fainted and hero.burned:
        change = apply_burn_damage(hero)
        result.append(change)
    if not hero.fainted and hero.frozen:
        change = apply_frozen_changes(hero, move)
        result.append(change)
    if not hero.fainted and hero.asleep:
        change = apply_asleep_changes(hero)
        result.append(change)
    return PostTurnResult(changes=result,
                          fainted=hero.fainted,
                          second_fainted=other_hero.fainted)


def apply_status_change(
        hero: UserHero,
        hero_mods: HeroMods,
        status: StatusEffect) -> list[StatusChangeResult]:
    result = []
    if status == StatusEffect.poisoned:
        effect = apply_poison_status(hero)
        result.append(StatusChangeResult(status=StatusEffect.poisoned, effect=effect))
    if status == StatusEffect.burn:
        effect = apply_burn_status(hero)
        result.append(StatusChangeResult(status=StatusEffect.burn, effect=effect))
    if status == StatusEffect.paralyzed:
        effect = apply_paralyzed_status(hero)
        result.append(StatusChangeResult(status=StatusEffect.paralyzed, effect=effect))
    if status == StatusEffect.leech_seed:
        hero_mods.leech_seed = True
        result.append(StatusChangeResult(
            status=StatusEffect.leech_seed,
            effect=StatusChangeEffect.success))
    if status == StatusEffect.asleep:
        hero.sleep_counter = random.randint(1, 6)
        hero_mods.asleep = True
        result.append(StatusChangeResult
                      (status=StatusEffect.sleep,
                       effect=StatusChangeEffect.success))
    if status == StatusEffect.frozen:
        effect = apply_frozen_status(hero)
        result.append(StatusChangeResult(status=StatusEffect.frozen, effect=effect))
    return result


def is_hero_able_to_move(hero: UserHero) -> MovementTestResult:
    if hero.paralyzed:
        rand = random.randint(0, 100)
        if rand < 25:
            return MovementTestResult(reason=StatusEffect.paralyzed)
    if hero.frozen:
        return MovementTestResult(reason=StatusEffect.frozen)
    if hero.asleep:
        return MovementTestResult(reason=StatusEffect.asleep)
    return MovementTestResult(able=True)


def get_item(move: MoveRequest, user_id: int, db: Session) -> Optional[Item]:
    if move.move != MoveType.item:
        return None
    item: EquipmentEntry = equipment_repo.get_item_entry(move.id, user_id, db)
    if item.amount < 1:
        return None
    if item.item.item_type not in [ItemType.battle_item, ItemType.pokeball]:
        return None
    item.amount = item.amount - 1
    return item.item


def switch_hero(
        battle: Battle,
        num: int,
        user_id: int,
        db: Session) -> Optional[UserHero]:
    team = team_repo.get_team(user_id, db)
    hero = None
    if num == 1:
        hero = team.hero_1
    elif num == 2:
        hero = team.hero_2
    elif num == 3:
        hero = team.hero_3
    elif num == 4:
        hero = team.hero_4
    elif num == 5:
        hero = team.hero_5
    elif num == 6:
        hero = team.hero_6
    if hero is None:
        return None
    if hero.id == battle.hero_id:
        return None
    battle.hero = hero
    mods: HeroMods = battle.hero_mods
    mods.speed = 0
    mods.attack = 0
    mods.defense = 0
    mods.evasion = 0
    mods.accuracy = 0
    mods.leech_seed = False
    return hero
