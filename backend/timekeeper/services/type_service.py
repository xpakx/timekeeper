from ..db.models import HeroType

type_table = {
        HeroType.air: {
            HeroType.air: 1.0,
            HeroType.fire: 2.0,
            HeroType.steam: 0.5,
            HeroType.water: 1.0,
            HeroType.earth: 0.5
            }
        }


def get_effectiveness(attacker: HeroType, attacked: HeroType) -> float:
    return type_table[attacker][attacked]
