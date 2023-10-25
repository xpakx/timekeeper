from .models import Hero, HeroEvolve
from sqlalchemy.orm import Session
import random
from typing import Optional
from sqlalchemy import and_

COMMON = range(1, 6)
UNCOMMON = range(6, 16)
RARE = range(16, 21)


def get_random_hero(db: Session) -> Optional[Hero]:
    rnd = random.randint(0, 6)
    if rnd < 3:
        rnd = random.choice(COMMON)
    elif rnd < 5:
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
