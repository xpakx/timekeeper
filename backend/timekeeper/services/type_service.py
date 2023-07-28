from ..db.models import HeroType


def get_effectiveness(attacker: HeroType, attacked: HeroType) -> float:
    if attacker == HeroType.air:
        if attacked == HeroType.air:
            return 1.0
        elif attacked == HeroType.fire:
            return 2.0
        elif attacked == HeroType.steam:
            return 0.5
        elif attacked == HeroType.water:
            return 1.0
        elif attacked == HeroType.earth:
            return 0.5
    return 1.0
