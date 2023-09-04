from ...db.models import Skill, UserHero, ExpGroup, MoveCategory
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
    return math.floor((4*lvl*lvl*lvl)/5)


def test_level_up(hero: UserHero, additional_levels: int = 1) -> bool:
    level = hero.level if hero.level else 0
    exp_needed = level_to_exp(
            hero.hero.exp_group,
            level + additional_levels)
    return level >= exp_needed


def check_level_change(hero: UserHero) -> int:
    level = hero.level if hero.level else 0
    for i in range(level+1, 101):
        if not test_level_up(hero, i):
            return i-1
    return 100


def calculate_if_player_moves_first(
        hero: UserHero,
        skill: Skill,
        hero_speed_stage: int,
        enemy: UserHero,
        enemy_skill: Skill,
        enemy_speed_stage: int,
        flee: bool = False,
        switch: bool = False) -> bool:
    if (switch):
        return True
    priority = 0 if flee else skill.priority
    if (priority > enemy_skill.priority):
        return True
    if (enemy_skill.priority > priority):
        return False
    speed = calculate_speed(hero) * stage_to_modifier(hero_speed_stage)
    enemy_speed = calculate_speed(enemy) * stage_to_modifier(enemy_speed_stage)
    return speed >= enemy_speed


def calculate_stat(base: int, iv: int, effort: int, lvl: int) -> int:
    return math.floor((2 * base + iv + effort) * lvl/100 + 5)


def calculate_hp(hero: UserHero) -> int:
    return math.floor(
            (2 * hero.hero.base_hp + hero.hp + 0)
            * hero.level/100 + hero.level + 10)


def calculate_speed(hero: UserHero):
    return calculate_stat(
            hero.hero.base_speed,
            hero.speed,
            0,
            hero.level)


def calculate_attack(hero: UserHero):
    return calculate_stat(
            hero.hero.base_attack,
            hero.attack,
            0,
            hero.level)


def calculate_defense(hero: UserHero):
    return calculate_stat(
            hero.hero.base_defense,
            hero.defense,
            0,
            hero.level)


def calculate_special_atk(hero: UserHero):
    return calculate_stat(
            hero.hero.base_special_attack,
            hero.special_attack,
            0,
            hero.level)


def calculate_special_def(hero: UserHero):
    return calculate_stat(
            hero.hero.base_special_defense,
            hero.special_defense,
            0,
            hero.level)


def test_accuracy(
        hero: UserHero,
        move: Skill,
        target: UserHero,
        hero_accuracy: int,
        target_evasion: int):
    stat_stage = hero_accuracy - target_evasion
    if stat_stage < -6:
        stat_stage = -6
    if stat_stage > 6:
        stat_stage = 6
    modifier = acc_stage_to_modifier(stat_stage)
    stat = move.accuracy*modifier
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


def test_crit(crit_mod: int) -> float:
    max = 16
    if crit_mod > 3:
        max = 2
    elif crit_mod == 3:
        max = 3
    elif crit_mod == 2:
        max = 4
    elif crit_mod == 1:
        max = 8
    return random(0, max) == 0


def calculate_damage(
        hero: UserHero,
        atk_stage: int,
        spec_atk_stage: int,
        move: Skill,
        enemy: UserHero,
        def_stage: int,
        spec_def_stage: int,
        critical: bool) -> int:
    level = hero.level
    attack = 0
    defense = 0
    if (move.move_category == MoveCategory.special):
        attack = stage_to_modifier(spec_atk_stage) * calculate_special_atk(hero)
        defense = stage_to_modifier(spec_def_stage) * calculate_special_def(enemy)
    else:
        attack = stage_to_modifier(atk_stage) * calculate_attack(hero)
        defense = stage_to_modifier(def_stage) * calculate_defense(enemy)
    stab = 1
    if (test_hero_move_type(hero, move)):
        stab = 1.5
    type_mod = get_effectiveness(move.move_type, enemy.hero)
    crit = 2 if critical else 1
    rand = random.randint(85, 101)/100
    return (math.floor(
            math.floor(
                math.floor((2*level)/5+2)
                * attack * move.power / defense)
            / 50) + 2)*crit*rand*stab*type_mod


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
