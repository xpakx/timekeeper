from ...db.models import HeroType, Hero
from typing import Optional

type_table = {
        HeroType.normal: {
            HeroType.rock: 0.5,
            HeroType.ghost: 0,
            HeroType.steel: 0.5
            },
        HeroType.fighting: {
            HeroType.normal: 2.0,
            HeroType.flying: 0.5,
            HeroType.poison: 0.5,
            HeroType.rock: 2.0,
            HeroType.bug: 0.5,
            HeroType.ghost: 0,
            HeroType.steel: 2.0,
            HeroType.psychic: 0.5,
            HeroType.ice: 2.0,
            HeroType.dark: 2.0
            },
        HeroType.flying: {
            HeroType.fighting: 2.0,
            HeroType.rock: 0.5,
            HeroType.bug: 2.0,
            HeroType.steel: 0.5,
            HeroType.grass: 2.0,
            HeroType.electric: 0.5
            },
        HeroType.poison: {
            HeroType.poison: 0.5,
            HeroType.ground: 0.5,
            HeroType.rock: 0.5,
            HeroType.ghost: 0.5,
            HeroType.steel: 0,
            HeroType.grass: 2.0
            },
        HeroType.ground: {
            HeroType.flying: 0,
            HeroType.poison: 2.0,
            HeroType.rock: 2.0,
            HeroType.bug: 0.5,
            HeroType.steel: 2.0,
            HeroType.fire: 2.0,
            HeroType.grass: 0.5,
            HeroType.electric: 1
            },
        HeroType.rock: {
            HeroType.fighting: 0.5,
            HeroType.flying: 2.0,
            HeroType.ground: 0.5,
            HeroType.bug: 2.0,
            HeroType.steel: 0.5,
            HeroType.fire: 2.0,
            HeroType.ice: 2.0
            },
        HeroType.bug: {
            HeroType.fighting: 0.5,
            HeroType.flying: 0.5,
            HeroType.poison: 0.5,
            HeroType.ghost: 0.5,
            HeroType.steel: 0.5,
            HeroType.fire: 0.5,
            HeroType.grass: 2.0,
            HeroType.psychic: 2.0,
            HeroType.dark: 2.0,
            },
        HeroType.ghost: {
            HeroType.normal: 0,
            HeroType.ghost: 2.0,
            HeroType.steel: 0.5,
            HeroType.psychic: 2.0,
            HeroType.dark: 0.5
            },
        HeroType.steel: {
            HeroType.rock: 2.0,
            HeroType.steel: 0.5,
            HeroType.fire: 0.5,
            HeroType.water: 0.5,
            HeroType.electric: 0.5,
            HeroType.ice: 2.0
            },
        HeroType.fire: {
            HeroType.rock: 0.5,
            HeroType.bug: 2.0,
            HeroType.steel: 2.0,
            HeroType.fire: 0.5,
            HeroType.water: 0.5,
            HeroType.grass: 2.0,
            HeroType.ice: 2.0,
            HeroType.dragon: 0.5
            },
        HeroType.water: {
            HeroType.ground: 2.0,
            HeroType.rock: 2.0,
            HeroType.fire: 2.0,
            HeroType.water: 0.5,
            HeroType.grass: 0.5,
            HeroType.dragon: 0.5
            },
        HeroType.grass: {
            HeroType.flying: 0.5,
            HeroType.poison: 0.5,
            HeroType.ground: 2.0,
            HeroType.rock: 2.0,
            HeroType.bug: 0.5,
            HeroType.steel: 0.5,
            HeroType.fire: 0.5,
            HeroType.water: 2.0,
            HeroType.ice: 0.5,
            HeroType.dragon: 0.5
            },
        HeroType.electric: {
            HeroType.flying: 2.0,
            HeroType.ground: 0,
            HeroType.water: 2.0,
            HeroType.grass: 0.5,
            HeroType.electric: 0.5,
            HeroType.dragon: 0.5
            },
        HeroType.psychic: {
            HeroType.fighting: 2.0,
            HeroType.poison: 2.0,
            HeroType.steel: 0.5,
            HeroType.psychic: 0.5,
            HeroType.dark: 0
            },
        HeroType.ice: {
            HeroType.flying: 2.0,
            HeroType.ground: 2.0,
            HeroType.steel: 0.5,
            HeroType.fire: 0.5,
            HeroType.water: 0.5,
            HeroType.grass: 2.0,
            HeroType.ice: 0.5,
            HeroType.dragon: 2.0
            },
        HeroType.dragon: {
            HeroType.steel: 0.5,
            HeroType.dragon: 2.0
            },
        HeroType.dark: {
            HeroType.fighting: 0.5,
            HeroType.ghost: 2.0,
            HeroType.steel: 0.5,
            HeroType.psychic: 2.0,
            HeroType.dark: 0.5
            }
        }


def get_effectiveness(attacker: HeroType, attacked: Hero) -> float:
    first_type = get_effectiveness_(attacker, attacked.hero_type)
    second_type = get_effectiveness_(attacker, attacked.secondary_hero_type)
    return first_type * second_type


def get_effectiveness_(
        attacker: HeroType,
        attacked: Optional[HeroType]) -> float:
    if not attacked:
        return 1.0
    if attacked in type_table[attacker]:
        return type_table[attacker][attacked]
    return 1.0
