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


level_dict = {
        ExpGroup.slow: {},
        ExpGroup.medium_slow: {},
        ExpGroup.medium_fast: {},
        ExpGroup.fast: {}
        }


for i in range(1, 101):
    level_dict[ExpGroup.slow][i] = level_to_exp(ExpGroup.slow, i)
    level_dict[ExpGroup.medium_slow][i] = level_to_exp(ExpGroup.medium_slow, i)
    level_dict[ExpGroup.medium_fast][i] = level_to_exp(ExpGroup.medium_fast, i)
    level_dict[ExpGroup.fast][i] = level_to_exp(ExpGroup.fast, i)


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
    for i in range(1, 101):
        if level_dict[group][i] > exp:
            return i-1
    return 100
