from ...db.models import Skill, UserHero, ExpGroup, MoveCategory, HeroMods
import math
import random
from .type_service import get_effectiveness


def level_to_exp(group: ExpGroup, lvl: int) -> int:
    if group == ExpGroup.slow:
        return math.floor((5*lvl*lvl*lvl)/4)
    if group == ExpGroup.medium_slow:
        return math.floor((6*lvl*lvl*lvl)/5 - 15*lvl*lvl + 100*lvl - 140)
    if group == ExpGroup.medium_fast:
        return lvl*lvl*lvl
    if group == ExpGroup.fast:
        return math.floor((4*lvl*lvl*lvl)/5)
    if group == ExpGroup.erratic:
        return calculate_exp_for_erratic_group(lvl)
    if group == ExpGroup.fluctuating:
        return calculate_exp_for_fluctuating_group(lvl)
    return 0


def calculate_exp_for_erratic_group(lvl: int) -> int:
    if lvl < 50:
        return math.floor((lvl*lvl*lvl*(100-lvl))/50)
    if lvl < 68:
        return math.floor((lvl*lvl*lvl*(150-lvl))/100)
    if lvl < 98:
        return math.floor((lvl*lvl*lvl*math.floor((1911-10*lvl)/3))/500)
    return math.floor((lvl*lvl*lvl*(160-lvl))/100)


def calculate_exp_for_fluctuating_group(lvl: int) -> int:
    if lvl < 15:
        return math.floor((lvl*lvl*lvl*(math.floor((lvl+1)/3)+24))/50)
    if lvl < 36:
        return math.floor((lvl*lvl*lvl*(lvl+14))/50)
    return math.floor((lvl*lvl*lvl*(math.floor(lvl/2)+32))/50)


def test_level_up(hero: UserHero, additional_levels: int = 1) -> bool:
    level = hero.level if hero.level else 0
    exp = hero.experience if hero.experience else 0
    exp_needed = level_to_exp(
            hero.hero.exp_group,
            level + additional_levels)
    return exp >= exp_needed


def check_level_change(hero: UserHero) -> int:
    level = hero.level if hero.level else 0
    for i in range(1, 101-level):
        if not test_level_up(hero, i):
            return level+i-1
    return 100


def calculate_if_player_moves_first(
        hero: UserHero,
        hero_mods: HeroMods,
        skill: Skill,
        enemy: UserHero,
        enemy_mods: HeroMods,
        enemy_skill: Skill,
        flee: bool = False,
        switch: bool = False) -> bool:
    if (switch):
        return True
    priority = 0
    if flee:
        priority = 0
    elif skill:
        priority = skill.priority
    enemy_priority = 0
    if enemy_skill:
        enemy_priority = enemy_skill.priority
    if (priority > enemy_priority):
        return True
    if (enemy_priority > priority):
        return False
    speed = calculate_speed(hero) * stage_to_modifier(hero_mods.speed)
    enemy_speed = calculate_speed(enemy) * stage_to_modifier(enemy_mods.speed)
    return speed >= enemy_speed


def calculate_stat(base: int, iv: int, effort: int, lvl: int) -> int:
    return math.floor((2 * base + iv + effort) * lvl/100 + 5)


def calculate_hp(hero: UserHero) -> int:
    return math.floor(
            (2 * hero.hero.base_hp + hero.hp + 0)
            * hero.level/100 + hero.level + 10)


def calculate_hp_(base_hp: int, hp: int, level: int) -> int:
    return math.floor(
            (2 * base_hp + hp + 0) * level/100 + level + 10)


def calculate_speed(hero: UserHero) -> int:
    speed = calculate_stat(
            hero.hero.base_speed,
            hero.speed,
            0,
            hero.level)
    if hero.paralyzed:
        return math.floor(speed/4)
    else:
        return speed


def calculate_attack(hero: UserHero) -> int:
    return calculate_stat(
            hero.hero.base_attack,
            hero.attack,
            0,
            hero.level)


def calculate_defense(hero: UserHero) -> int:
    return calculate_stat(
            hero.hero.base_defense,
            hero.defense,
            0,
            hero.level)


def calculate_special_atk(hero: UserHero) -> int:
    return calculate_stat(
            hero.hero.base_special_attack,
            hero.special_attack,
            0,
            hero.level)


def calculate_special_def(hero: UserHero) -> int:
    return calculate_stat(
            hero.hero.base_special_defense,
            hero.special_defense,
            0,
            hero.level)


def test_accuracy(
        hero: UserHero,
        hero_mods: HeroMods,
        move: Skill,
        target: UserHero,
        target_mods: HeroMods) -> bool:
    stat_stage = hero_mods.accuracy - target_mods.evasion
    if stat_stage < -6:
        stat_stage = -6
    if stat_stage > 6:
        stat_stage = 6
    modifier = acc_stage_to_modifier(stat_stage)
    stat = move.accuracy*modifier if move else 100
    return random.randint(0, 100) < stat


def acc_stage_to_modifier(stage: int) -> float:
    if stage < 0:
        stage = -1 * stage
        return 3/(stage+3)
    if stage > 0:
        return (3+stage)/3
    return 1


def stage_to_modifier(stage: int) -> float:
    if stage < 0:
        stage = -1 * stage
        return 2/(stage+2)
    if stage > 0:
        return (2+stage)/2
    return 1


def test_crit(crit_mod: int) -> bool:
    max = 16
    if crit_mod > 3:
        max = 2
    elif crit_mod == 3:
        max = 3
    elif crit_mod == 2:
        max = 4
    elif crit_mod == 1:
        max = 8
    return random.randint(0, max) == 0


def calculate_damage(
        hero: UserHero,
        hero_mods: HeroMods,
        move: Skill,
        enemy: UserHero,
        enemy_mods: HeroMods,
        critical: bool) -> int:
    if not move:
        return 0
    level = hero.level
    attack = calculate_current_attack(hero, hero_mods, move, enemy, enemy_mods)
    defense = calculate_current_defense(hero, hero_mods, move, enemy, enemy_mods)
    stab = calculate_stab_factor(hero, move)
    type_mod = get_effectiveness(move.move_type, enemy.hero)
    crit = 2 if critical else 1
    rand = random.randint(85, 101)/100
    dmg = (math.floor(
            math.floor(
                math.floor((2*level)/5+2)
                * attack * move.power / defense)
            / 50) + 2)*crit*rand*stab*type_mod
    if hero.burned and move.move_category == MoveCategory.physical:
        return math.floor(dmg/2)
    else:
        return dmg


def test_hero_move_type(hero: UserHero, move: Skill) -> bool:
    return (
            (
                hero.hero.hero_type
                and
                hero.hero.hero_type == move.move_type)
            or
            (
                hero.hero.secondary_hero_type
                and
                hero.hero.secondary_hero_type == move.move_type
            )
        )


def calculate_current_attack(
        hero: UserHero,
        hero_mods: HeroMods,
        move: Skill,
        enemy: UserHero,
        enemy_mods: HeroMods,
        ) -> int:
    if (move.move_category == MoveCategory.special):
        return stage_to_modifier(hero_mods.special_attack) *\
            calculate_special_atk(hero)
    return stage_to_modifier(hero_mods.attack) *\
        calculate_attack(hero)


def calculate_current_defense(
        hero: UserHero,
        hero_mods: HeroMods,
        move: Skill,
        enemy: UserHero,
        enemy_mods: HeroMods,
        ) -> int:
    if (move.move_category == MoveCategory.special):
        return stage_to_modifier(enemy_mods.special_defense) *\
            calculate_special_def(enemy)
    return stage_to_modifier(enemy_mods.defense) *\
        calculate_defense(enemy)


def calculate_stab_factor(hero: UserHero, move: Skill) -> float:
    if (test_hero_move_type(hero, move)):
        return 1.5
    return 1


def test_fleeing(hero: UserHero, hero_mods: HeroMods, enemy: UserHero, enemy_mods: HeroMods) -> bool:
    hero_speed = calculate_speed(hero)
    hero_modified_speed = hero_speed * stage_to_modifier(hero_mods.speed)
    enemy_speed = calculate_speed(enemy)
    enemy_modified_speed = enemy_speed * stage_to_modifier(enemy_mods.speed)
    attempts = hero_mods.flee_attempts + 1
    if hero_modified_speed >= enemy_modified_speed:
        return True
    odds = (math.floor((hero_speed*128)/enemy_speed) + 30*attempts) % 256
    rand = random.randint(85, 101)
    return rand < odds
