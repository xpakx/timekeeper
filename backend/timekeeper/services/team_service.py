from ..db import user_hero_repo, team_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models import Team, UserHero
from typing import Optional


def get_team(user_id: int, db: Session) -> Team:
    team = team_repo.get_team(user_id, db)
    if team is None:
        raise no_team_object_exception()
    return team


def add_hero(user_id: int, hero_id: int, num: int, db: Session) -> Team:
    team = team_repo.get_team(user_id, db)
    if team is None:
        raise no_team_object_exception()
    hero: Optional[UserHero] = user_hero_repo.get_hero(user_id, hero_id, db)
    if hero is None:
        raise no_such_hero_exception()
    if num == 1:
        team.hero_1_id = hero.id
    elif num == 2:
        team.hero_2_id = hero.id
    elif num == 3:
        team.hero_3_id = hero.id
    elif num == 4:
        team.hero_4_id = hero.id
    elif num == 5:
        team.hero_5_id = hero.id
    elif num == 6:
        team.hero_6_id = hero.id
    db.commit()
    db.refresh(team)
    return team


def no_team_object_exception():
    return HTTPException(
        status_code=501,
        detail="No team object!",
    )


def no_such_hero_exception():
    return HTTPException(
        status_code=400,
        detail="No such hero!",
    )
