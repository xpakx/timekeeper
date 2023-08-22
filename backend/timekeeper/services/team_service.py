from ..db import user_hero_repo, team_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models import Team, UserHero
from typing import Optional
from ..routers.dto.team_schemas import TeamRequest, TeamAction, TeamResponse


def get_team(user_id: int, db: Session) -> TeamResponse:
    team = team_repo.get_team(user_id, db)
    if team is None:
        raise no_team_object_exception()
    return TeamResponse.transform_data(team)


def change_team(user_id: int, request: TeamRequest, db: Session) -> Team:
    if request.action != TeamAction.add:
        return add_hero(user_id, request, db)
    else:
        return switch_heroes(user_id, request, db)


def add_hero(user_id: int, request: TeamRequest, db: Session) -> Team:
    team = team_repo.get_team(user_id, db)
    if team is None:
        raise no_team_object_exception()
    hero: Optional[UserHero] = user_hero_repo.get_hero(
            user_id,
            request.hero_id,
            db
            )
    if hero is None:
        raise no_such_hero_exception()
    if hero.incubated or hero.in_team:
        raise hero_not_available_exception()
    num = request.num
    if num == 1:
        team.hero_1_id.in_team = False
        team.hero_1_id = hero.id
    elif num == 2:
        team.hero_2_id.in_team = False
        team.hero_2_id = hero.id
    elif num == 3:
        team.hero_3_id.in_team = False
        team.hero_3_id = hero.id
    elif num == 4:
        team.hero_4_id.in_team = False
        team.hero_4_id = hero.id
    elif num == 5:
        team.hero_5_id.in_team = False
        team.hero_5_id = hero.id
    elif num == 6:
        team.hero_6_id.in_team = False
        team.hero_6_id = hero.id
    hero.in_team = True
    db.commit()
    db.refresh(team)
    return team


def switch_heroes(user_id: int, request: TeamRequest, db: Session) -> Team:
    team = team_repo.get_team(user_id, db)
    if team is None:
        raise no_team_object_exception()
    hero: Optional[UserHero] = user_hero_repo.get_hero(
            user_id,
            request.hero_id,
            db
            )
    if hero is None:
        raise no_such_hero_exception()
    if hero.incubated or not hero.in_team:
        raise hero_not_available_exception()
    num = request.switch_num
    secondary_hero_id: Optional[int] = None
    if num == 1:
        secondary_hero_id = team.hero_1_id
        team.hero_1_id = hero.id
    elif num == 2:
        secondary_hero_id = team.hero_2_id
        team.hero_2_id = hero.id
    elif num == 3:
        secondary_hero_id = team.hero_3_id
        team.hero_3_id = hero.id
    elif num == 4:
        secondary_hero_id = team.hero_4_id
        team.hero_4_id = hero.id
    elif num == 5:
        secondary_hero_id = team.hero_5_id
        team.hero_5_id = hero.id
    elif num == 6:
        secondary_hero_id = team.hero_6_id
        team.hero_6_id = hero.id
    num = request.num
    if num == 1:
        team.hero_1_id = secondary_hero_id
    elif num == 2:
        team.hero_2_id = secondary_hero_id
    elif num == 3:
        team.hero_3_id = secondary_hero_id
    elif num == 4:
        team.hero_4_id = secondary_hero_id
    elif num == 5:
        team.hero_5_id = secondary_hero_id
    elif num == 6:
        team.hero_6_id = secondary_hero_id
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


def hero_not_available_exception():
    return HTTPException(
        status_code=400,
        detail="Hero unavailable!",
    )
