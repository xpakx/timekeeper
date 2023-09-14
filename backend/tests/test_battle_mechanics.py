from timekeeper.db.models import ExpGroup, UserHero, Hero, Skill, HeroMods
import timekeeper.services.mechanics.battle_mech_service as service
from unittest.mock import patch, Mock


# calculating experience
def test_1th_lvl_to_exp_for_medium_slow_group():
    result = service.level_to_exp(ExpGroup.medium_slow, 1)
    assert result == -54


def test_100th_lvl_to_exp_for_medium_slow_group():
    result = service.level_to_exp(ExpGroup.medium_slow, 100)
    assert result == 1_059_860


def test_25th_lvl_to_exp_for_medium_slow_group():
    result = service.level_to_exp(ExpGroup.medium_slow, 25)
    assert result == 11_735


def test_1th_lvl_to_exp_for_slow_group():
    result = service.level_to_exp(ExpGroup.slow, 1)
    assert result == 1


def test_100th_lvl_to_exp_for_slow_group():
    result = service.level_to_exp(ExpGroup.slow, 100)
    assert result == 1_250_000


def test_25th_lvl_to_exp_for_slow_group():
    result = service.level_to_exp(ExpGroup.slow, 25)
    assert result == 19_531


def test_1th_lvl_to_exp_for_medium_fast_group():
    result = service.level_to_exp(ExpGroup.medium_fast, 1)
    assert result == 1


def test_100th_lvl_to_exp_for_medium_fast_group():
    result = service.level_to_exp(ExpGroup.medium_fast, 100)
    assert result == 1_000_000


def test_25th_lvl_to_exp_for_medium_fast_group():
    result = service.level_to_exp(ExpGroup.medium_fast, 25)
    assert result == 15_625


def test_1th_lvl_to_exp_for_fast_group():
    result = service.level_to_exp(ExpGroup.fast, 1)
    assert result == 0


def test_100th_lvl_to_exp_for_fast_group():
    result = service.level_to_exp(ExpGroup.fast, 100)
    assert result == 800_000


def test_25th_lvl_to_exp_for_fast_group():
    result = service.level_to_exp(ExpGroup.fast, 25)
    assert result == 12_500


def test_1th_lvl_to_exp_for_erratic_group():
    result = service.level_to_exp(ExpGroup.erratic, 1)
    assert result == 1


def test_100th_lvl_to_exp_for_erratic_group():
    result = service.level_to_exp(ExpGroup.erratic, 100)
    assert result == 600_000


def test_25th_lvl_to_exp_for_erratic_group():
    result = service.level_to_exp(ExpGroup.erratic, 25)
    assert result == 23_437


def test_1th_lvl_to_exp_for_fluctuating_group():
    result = service.level_to_exp(ExpGroup.fluctuating, 1)
    assert result == 0


def test_100th_lvl_to_exp_for_fluctuating_group():
    result = service.level_to_exp(ExpGroup.fluctuating, 100)
    assert result == 1_640_000


def test_25th_lvl_to_exp_for_fluctuating_group():
    result = service.level_to_exp(ExpGroup.fluctuating, 25)
    assert result == 12_187


# testing level up
def test_level_up_without_enough_experience():
    hero = UserHero(
            hero=Hero(
                exp_group=ExpGroup.fast
                ),
            experience=22,
            level=3
            )
    result = service.test_level_up(hero, 1)
    assert not result


def test_level_up():
    hero = UserHero(
            hero=Hero(
                exp_group=ExpGroup.fast
                ),
            experience=52,
            level=3
            )
    result = service.test_level_up(hero, 1)
    assert result


def test_level_up_multiple_levels():
    hero = UserHero(
            hero=Hero(
                exp_group=ExpGroup.fast
                ),
            experience=800,
            level=3
            )
    result = service.test_level_up(hero, 5)
    assert result


def test_level_up_multiple_levels_without_enough_experience():
    hero = UserHero(
            hero=Hero(
                exp_group=ExpGroup.fast
                ),
            experience=800,
            level=3
            )
    result = service.test_level_up(hero, 10)
    assert not result


# checking level change
def test_level_change_without_level_up():
    hero = UserHero(
            hero=Hero(
                exp_group=ExpGroup.fast
                ),
            experience=1800,
            level=13
            )
    result = service.check_level_change(hero)
    assert result == 13


def test_level_change_with_level_up():
    hero = UserHero(
            hero=Hero(
                exp_group=ExpGroup.fast
                ),
            experience=1800,
            level=9
            )
    result = service.check_level_change(hero)
    assert result == 13


def test_level_change_at_level_100():
    hero = UserHero(
            hero=Hero(
                exp_group=ExpGroup.fast
                ),
            experience=1_000_000,
            level=100
            )
    result = service.check_level_change(hero)
    assert result == 100


# calculating move order
def test_move_order_while_switching():
    hero = UserHero(hero=Hero(base_speed=100), speed=30, level=15)
    hero_mods = HeroMods(speed=6)
    enemy = UserHero(hero=Hero(base_speed=1), speed=0, level=15)
    enemy_mods = HeroMods(speed=-6)
    enemy_skill = Skill(priority=0)
    result = service.calculate_if_player_moves_first(
            hero,
            hero_mods,
            None,
            enemy,
            enemy_mods,
            enemy_skill,
            switch=True)
    assert result


def test_move_order_with_different_priority():
    hero = UserHero(hero=Hero(base_speed=100), speed=30, level=15)
    hero_mods = HeroMods(speed=6)
    hero_skill = Skill(priority=3)
    enemy = UserHero(hero=Hero(base_speed=1), speed=0, level=15)
    enemy_mods = HeroMods(speed=-6)
    enemy_skill = Skill(priority=4)
    result = service.calculate_if_player_moves_first(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods,
            enemy_skill)
    assert not result


def test_move_order_with_flee_vs_positive_priority():
    hero = UserHero(hero=Hero(base_speed=100), speed=30, level=15)
    hero_mods = HeroMods(speed=6)
    enemy = UserHero(hero=Hero(base_speed=100), speed=30, level=15)
    enemy_mods = HeroMods(speed=6)
    enemy_skill = Skill(priority=3)
    result = service.calculate_if_player_moves_first(
            hero,
            hero_mods,
            None,
            enemy,
            enemy_mods,
            enemy_skill,
            flee=True)
    assert not result


def test_move_order_with_flee_vs_negative_priority():
    hero = UserHero(hero=Hero(base_speed=100), speed=30, level=15)
    hero_mods = HeroMods(speed=6)
    hero_skill = Skill(priority=3)
    enemy = UserHero(hero=Hero(base_speed=100), speed=30, level=15)
    enemy_mods = HeroMods(speed=6)
    enemy_skill = Skill(priority=-3)
    result = service.calculate_if_player_moves_first(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods,
            enemy_skill,
            flee=True)
    assert result


def test_move_order_with_same_priority_and_different_base_speed():
    hero = UserHero(hero=Hero(base_speed=100), speed=30, level=15)
    hero_mods = HeroMods(speed=6)
    hero_skill = Skill(priority=0)
    enemy = UserHero(hero=Hero(base_speed=110), speed=30, level=15)
    enemy_mods = HeroMods(speed=6)
    enemy_skill = Skill(priority=0)
    result = service.calculate_if_player_moves_first(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods,
            enemy_skill)
    assert not result


def test_move_order_with_same_priority_and_different_speed():
    hero = UserHero(hero=Hero(base_speed=100), speed=0, level=15)
    hero_mods = HeroMods(speed=6)
    hero_skill = Skill(priority=0)
    enemy = UserHero(hero=Hero(base_speed=100), speed=30, level=15)
    enemy_mods = HeroMods(speed=6)
    enemy_skill = Skill(priority=0)
    result = service.calculate_if_player_moves_first(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods,
            enemy_skill)
    assert not result


def test_move_order_with_same_priority_and_different_level():
    hero = UserHero(hero=Hero(base_speed=100), speed=0, level=15)
    hero_mods = HeroMods(speed=6)
    hero_skill = Skill(priority=0)
    enemy = UserHero(hero=Hero(base_speed=100), speed=0, level=16)
    enemy_mods = HeroMods(speed=6)
    enemy_skill = Skill(priority=0)
    result = service.calculate_if_player_moves_first(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods,
            enemy_skill)
    assert not result


def test_move_order_with_same_priority_and_different_stat_stages():
    hero = UserHero(hero=Hero(base_speed=100), speed=0, level=15)
    hero_mods = HeroMods(speed=5)
    hero_skill = Skill(priority=0)
    enemy = UserHero(hero=Hero(base_speed=100), speed=0, level=15)
    enemy_mods = HeroMods(speed=6)
    enemy_skill = Skill(priority=0)
    result = service.calculate_if_player_moves_first(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods,
            enemy_skill)
    assert not result


def test_move_order_with_same_priority_and_stats():
    hero = UserHero(hero=Hero(base_speed=100), speed=0, level=15)
    hero_mods = HeroMods(speed=6)
    hero_skill = Skill(priority=0)
    enemy = UserHero(hero=Hero(base_speed=100), speed=0, level=15)
    enemy_mods = HeroMods(speed=6)
    enemy_skill = Skill(priority=0)
    result = service.calculate_if_player_moves_first(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods,
            enemy_skill)
    assert result


# accuracy test
@patch('random.randint', Mock(return_value=60))
def test_successful_accuracy_check():
    hero = UserHero()
    hero_mods = HeroMods(accuracy=0)
    hero_skill = Skill(accuracy=70)
    enemy = UserHero()
    enemy_mods = HeroMods(evasion=0)
    result = service.test_accuracy(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods)
    assert result


@patch('random.randint', Mock(return_value=71))
def test_failed_accuracy_check():
    hero = UserHero()
    hero_mods = HeroMods(accuracy=0)
    hero_skill = Skill(accuracy=70)
    enemy = UserHero()
    enemy_mods = HeroMods(evasion=0)
    result = service.test_accuracy(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods)
    assert not result


@patch('random.randint', Mock(return_value=31))
def test_failed_accuracy_check_with_minus_six_stage():
    hero = UserHero()
    hero_mods = HeroMods(accuracy=-3)
    hero_skill = Skill(accuracy=90)
    enemy = UserHero()
    enemy_mods = HeroMods(evasion=3)
    result = service.test_accuracy(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods)
    assert not result


@patch('random.randint', Mock(return_value=30))
def test_successful_accuracy_check_with_minus_six_stage():
    hero = UserHero()
    hero_mods = HeroMods(accuracy=-3)
    hero_skill = Skill(accuracy=90)
    enemy = UserHero()
    enemy_mods = HeroMods(evasion=3)
    result = service.test_accuracy(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods)
    assert not result


@patch('random.randint', Mock(return_value=30))
def test_if_stage_for_accuracy_check_is_capped_at_minus_six():
    hero = UserHero()
    hero_mods = HeroMods(accuracy=-6)
    hero_skill = Skill(accuracy=90)
    enemy = UserHero()
    enemy_mods = HeroMods(evasion=6)
    result = service.test_accuracy(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods)
    assert not result


@patch('random.randint', Mock(return_value=90))
def test_failed_accuracy_check_with_six_stage():
    hero = UserHero()
    hero_mods = HeroMods(accuracy=3)
    hero_skill = Skill(accuracy=30)
    enemy = UserHero()
    enemy_mods = HeroMods(evasion=-3)
    result = service.test_accuracy(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods)
    assert not result


@patch('random.randint', Mock(return_value=89))
def test_successful_accuracy_check_with_six_stage():
    hero = UserHero()
    hero_mods = HeroMods(accuracy=3)
    hero_skill = Skill(accuracy=30)
    enemy = UserHero()
    enemy_mods = HeroMods(evasion=-3)
    result = service.test_accuracy(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods)
    assert result


@patch('random.randint', Mock(return_value=90))
def test_if_stage_for_accuracy_check_is_capped_at_six():
    hero = UserHero()
    hero_mods = HeroMods(accuracy=6)
    hero_skill = Skill(accuracy=30)
    enemy = UserHero()
    enemy_mods = HeroMods(evasion=-6)
    result = service.test_accuracy(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods)
    assert not result
