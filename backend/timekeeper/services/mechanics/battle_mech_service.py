from ...db.models import Skill, UserHero, ExpGroup
import math


def level_to_exp(group: ExpGroup, lvl: int) -> int:
    if group == ExpGroup.slow:
        return math.floor((5*lvl*lvl*lvl)/4)
    if group == ExpGroup.medium_slow:
        return math.floor((6*lvl*lvl*lvl)/5 - 15*lvl*lvl + 100*lvl - 140)
    if group == ExpGroup.medium_fast:
        return lvl*lvl*lvl
    if group == ExpGroup.fast:
        return math.floor((4*lvl*lvl*lvl)/5)


def test_level_up(hero: UserHero, additional_levels: int = 1) -> bool:
    exp_needed = level_to_exp(
            hero.hero.exp_group,
            hero.level + additional_levels)
    return hero.level >= exp_needed


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
