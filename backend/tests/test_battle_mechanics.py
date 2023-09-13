from timekeeper.db.models import ExpGroup, UserHero, Hero
import timekeeper.services.mechanics.battle_mech_service as service


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
