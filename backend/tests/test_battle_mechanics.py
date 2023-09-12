from timekeeper.db.models import ExpGroup
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
