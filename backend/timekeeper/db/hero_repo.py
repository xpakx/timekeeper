from .models import Hero, HeroEvolve, Encounter
from sqlalchemy.orm import Session, joinedload
import random
from typing import Optional
from sqlalchemy import and_
from functools import reduce

COMMON = [10, 13, 16, 19]
UNCOMMON = [11, 14, 17, 20]
RARE = [1, 4, 7]
STARTER = [1, 4, 7]


def get_random_hero(db: Session, starter: bool = False) -> Optional[Hero]:
    rnd = 0
    if starter:
        rnd = get_random_starter_id()
    else:
        rnd = get_random_id()

    return db\
        .query(Hero)\
        .where(
              Hero.num == rnd
            )\
        .first()


def get_random_id() -> int:
    rnd = random.randint(0, 100)
    if rnd < 74:
        return random.choice(COMMON)
    elif rnd < 94:
        return random.choice(UNCOMMON)
    else:
        return random.choice(RARE)


def get_random_hero_for_encounter(db: Session, battle_pass_id: int) -> Optional[Hero]:
    rnd = 0
    encounters = db\
        .query(Encounter)\
        .where(
              Encounter.item_id == battle_pass_id
            )\
        .all()
    max = reduce(lambda x, y: x + y.rate, encounters, 0)
    rnd = random.randint(0, max)
    cumulative_rate = 0
    for encounter in encounters:
        cumulative_rate += encounter.rate
        if rnd < cumulative_rate:
            return encounter.hero
    return None


def get_random_starter_id() -> int:
    return random.choice(STARTER)


def get_evolving_pair(
        hero_id: int,
        second_hero_id: int,
        db: Session) -> Optional[HeroEvolve]:
    entry: HeroEvolve = db\
        .query(HeroEvolve)\
        .where(
                and_(HeroEvolve.hero_id == hero_id,
                     HeroEvolve.evolve_id == second_hero_id)
                )\
        .first()
    return entry


def get_evolving_pairs_for_level(
        hero_id: int,
        level: int,
        db: Session) -> list[HeroEvolve]:
    entry: list[HeroEvolve] = db\
        .query(HeroEvolve)\
        .where(
                and_(HeroEvolve.hero_id == hero_id,
                     HeroEvolve.min_level <= level)
                )\
        .options(joinedload(HeroEvolve.evolve))\
        .all()
    return entry
