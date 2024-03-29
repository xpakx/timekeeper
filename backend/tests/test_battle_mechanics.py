from timekeeper.db.models import (
        ExpGroup,
        UserHero,
        Hero,
        Skill,
        HeroMods,
        HeroType,
        MoveCategory)
import timekeeper.services.mechanics.battle_mech_service as service
from unittest.mock import patch, Mock
from pytest import approx


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


@patch('random.randint', Mock(return_value=99))
def test_accuracy_check_with_100_accuracy():
    hero = UserHero()
    hero_mods = HeroMods(accuracy=0)
    hero_skill = Skill(accuracy=100)
    enemy = UserHero()
    enemy_mods = HeroMods(evasion=0)
    result = service.test_accuracy(
            hero,
            hero_mods,
            hero_skill,
            enemy,
            enemy_mods)
    assert result


# check STAB
def test_stab_while_different_types():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.water,
                secondary_hero_type=HeroType.grass))
    hero_skill = Skill(move_type=HeroType.fire)
    result = service.test_hero_move_type(hero, hero_skill)
    assert not result


def test_stab_with_only_first_type_exists_and_is_different():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.water,
                secondary_hero_type=None))
    hero_skill = Skill(move_type=HeroType.fire)
    result = service.test_hero_move_type(hero, hero_skill)
    assert not result


def test_stab_without_types():
    hero = UserHero(
            hero=Hero(
                hero_type=None,
                secondary_hero_type=None))
    hero_skill = Skill(move_type=HeroType.fire)
    result = service.test_hero_move_type(hero, hero_skill)
    assert not result


def test_stab_with_only_first_type():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.fire,
                secondary_hero_type=None))
    hero_skill = Skill(move_type=HeroType.fire)
    result = service.test_hero_move_type(hero, hero_skill)
    assert result


def test_stab_with_first_type_match():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.fire,
                secondary_hero_type=HeroType.grass))
    hero_skill = Skill(move_type=HeroType.fire)
    result = service.test_hero_move_type(hero, hero_skill)
    assert result


def test_stab_with_second_type_match():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.water,
                secondary_hero_type=HeroType.fire))
    hero_skill = Skill(move_type=HeroType.fire)
    result = service.test_hero_move_type(hero, hero_skill)
    assert result


# calculating damage
def test_damage_calc():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.water,
                secondary_hero_type=HeroType.fire,
                base_attack=100),
            level=5,
            attack=10)
    hero_mods = HeroMods(attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.water,
                secondary_hero_type=HeroType.fire,
                base_defense=50),
            level=5,
            defense=10)
    enemy_mods = HeroMods(defense=0)
    skill = Skill(
            move_type=HeroType.grass,
            move_category=MoveCategory.physical,
            power=10)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            False)
    assert isinstance(result, float)


@patch('random.randint', Mock(return_value=100))
def test_damage_calculation_with_physical_attack():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.water,
                secondary_hero_type=None,
                base_attack=20),
            level=10,
            attack=0)
    hero_mods = HeroMods(attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_defense=10),
            level=10,
            defense=0)
    enemy_mods = HeroMods(defense=0)
    skill = Skill(
            move_type=HeroType.grass,
            move_category=MoveCategory.physical,
            power=350)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            False)
    assert result == approx(56.0)


@patch('random.randint', Mock(return_value=100))
def test_damage_calculation_with_special_attack():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.water,
                secondary_hero_type=None,
                base_special_attack=20),
            level=10,
            special_attack=0)
    hero_mods = HeroMods(special_attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_special_defense=10),
            level=10,
            special_defense=0)
    enemy_mods = HeroMods(special_defense=0)
    skill = Skill(
            move_type=HeroType.grass,
            move_category=MoveCategory.special,
            power=350)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            False)
    assert result == approx(56.0)


@patch('random.randint', Mock(return_value=100))
def test_damage_calculation_with_same_type_attack():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.grass,
                secondary_hero_type=None,
                base_attack=20),
            level=10,
            attack=0)
    hero_mods = HeroMods(attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_defense=10),
            level=10,
            defense=0)
    enemy_mods = HeroMods(defense=0)
    skill = Skill(
            move_type=HeroType.grass,
            move_category=MoveCategory.physical,
            power=350)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            False)
    assert result == approx(84.0)


@patch('random.randint', Mock(return_value=100))
def test_damage_calculation_with_super_effective_move():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_attack=20),
            level=10,
            attack=0)
    hero_mods = HeroMods(attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.grass,
                secondary_hero_type=None,
                base_defense=10),
            level=10,
            defense=0)
    enemy_mods = HeroMods(defense=0)
    skill = Skill(
            move_type=HeroType.fire,
            move_category=MoveCategory.physical,
            power=350)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            False)
    assert result == approx(112.0)


@patch('random.randint', Mock(return_value=100))
def test_damage_calculation_with_not_very_effective_move():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_attack=20),
            level=10,
            attack=0)
    hero_mods = HeroMods(attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.water,
                secondary_hero_type=None,
                base_defense=10),
            level=10,
            defense=0)
    enemy_mods = HeroMods(defense=0)
    skill = Skill(
            move_type=HeroType.fire,
            move_category=MoveCategory.physical,
            power=350)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            False)
    assert result == approx(28.0)


@patch('random.randint', Mock(return_value=100))
def test_damage_calculation_with_invulnerable_type():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_attack=20),
            level=10,
            attack=0)
    hero_mods = HeroMods(attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.ghost,
                secondary_hero_type=None,
                base_defense=10),
            level=10,
            defense=0)
    enemy_mods = HeroMods(defense=0)
    skill = Skill(
            move_type=HeroType.normal,
            move_category=MoveCategory.physical,
            power=350)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            False)
    assert result == approx(0.0)


@patch('random.randint', Mock(return_value=100))
def test_damage_calculation_with_both_weakness_and_strength():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_attack=20),
            level=10,
            attack=0)
    hero_mods = HeroMods(attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.grass,
                secondary_hero_type=HeroType.water,
                base_defense=10),
            level=10,
            defense=0)
    enemy_mods = HeroMods(defense=0)
    skill = Skill(
            move_type=HeroType.fire,
            move_category=MoveCategory.physical,
            power=350)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            False)
    assert result == approx(56.0)


@patch('random.randint', Mock(return_value=100))
def test_damage_calculation_with_double_super_effective_move():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_attack=20),
            level=10,
            attack=0)
    hero_mods = HeroMods(attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.grass,
                secondary_hero_type=HeroType.bug,
                base_defense=10),
            level=10,
            defense=0)
    enemy_mods = HeroMods(defense=0)
    skill = Skill(
            move_type=HeroType.fire,
            move_category=MoveCategory.physical,
            power=350)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            False)
    assert result == approx(224.0)


@patch('random.randint', Mock(return_value=100))
def test_damage_calculation_with_critical_hit():
    hero = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_attack=20),
            level=10,
            attack=0)
    hero_mods = HeroMods(attack=0)
    enemy = UserHero(
            hero=Hero(
                hero_type=HeroType.normal,
                secondary_hero_type=None,
                base_defense=10),
            level=10,
            defense=0)
    enemy_mods = HeroMods(defense=0)
    skill = Skill(
            move_type=HeroType.fire,
            move_category=MoveCategory.physical,
            power=350)
    result = service.calculate_damage(
            hero,
            hero_mods,
            skill,
            enemy,
            enemy_mods,
            True)
    assert result == approx(112.0)
