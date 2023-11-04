from .models import Hero, HeroEvolve
from sqlalchemy.orm import Session
import random
from typing import Optional
from sqlalchemy import and_

COMMON = [10, 13, 16, 19]
UNCOMMON = [11, 14, 17, 20]
RARE = [1, 4, 7]


def get_random_hero(db: Session) -> Optional[Hero]:
    rnd = random.randint(0, 100)
    if rnd < 74:
        rnd = random.choice(COMMON)
    elif rnd < 94:
        rnd = random.choice(UNCOMMON)
    else:
        rnd = random.choice(RARE)

    return db\
        .query(Hero)\
        .where(
              Hero.num == rnd
            )\
        .first()


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
        .all()
    return entry
