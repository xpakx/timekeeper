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
    old_hero = insert_hero(hero, request.num, team)
    if old_hero:
        old_hero.in_team = False
    test_for_gap(team)
    db.commit()
    db.refresh(team)
    return team


def insert_hero(hero: Optional[UserHero], num: int, team: Team) -> UserHero:
    hero_id = hero.id if hero else None
    if num == 1:
        result = team.hero_1
        team.hero_1_id = hero_id
        team.hero_1 = hero
        return result
    if num == 2:
        result = team.hero_2
        team.hero_2_id = hero_id
        team.hero_2 = hero
        return result
    if num == 3:
        result = team.hero_3
        team.hero_3_id = hero_id
        team.hero_3 = hero
        return result
    if num == 4:
        result = team.hero_4
        team.hero_4_id = hero_id
        team.hero_4 = hero
        return result
    if num == 5:
        result = team.hero_5
        team.hero_5_id = hero_id
        team.hero_5 = hero
        return result
    if num == 6:
        result = team.hero_6
        team.hero_6_id = hero_id
        team.hero_6 = hero
        return result


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
    secondary_hero = insert_hero(hero, request.switch_num, team)
    insert_hero(secondary_hero, request.num, team)
    test_for_gap(team)
    db.commit()
    db.refresh(team)
    return team


def delete_hero(user_id: int, num: int, db: Session):
    team = team_repo.get_team(user_id, db)
    if team is None:
        raise no_team_object_exception()
    insert_hero(None, num, team)
    move_up(num, team)
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


def gap_in_team_exception():
    return HTTPException(
        status_code=400,
        detail="Team cannot have gaps!",
    )


def test_for_gap(team: Team):
    team_list = [
            team.hero_1,
            team.hero_2,
            team.hero_3,
            team.hero_4,
            team.hero_5,
            team.hero_6
            ]
    initial_gap_ended = False
    for i in reversed(team_list):
        if initial_gap_ended and not i:
            raise gap_in_team_exception
        if i and not initial_gap_ended:
            initial_gap_ended = True


def move_up(num: int, team: Team):
    if num < 2:
        team.hero_1 = team.hero_2
    if num < 3:
        team.hero_2 = team.hero_3
    if num < 4:
        team.hero_3 = team.hero_4
    if num < 5:
        team.hero_4 = team.hero_5
    if num < 6:
        team.hero_5 = team.hero_6
    team.hero_6 = None
