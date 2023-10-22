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
    if request.action == TeamAction.add:
        return add_hero(user_id, request, db)
    elif request.action == TeamAction.switch:
        return switch_heroes(user_id, request, db)
    elif request.action == TeamAction.delete:
        return delete_hero(user_id, request.num, db)


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
    hero.in_team = True
    old_hero = insert_hero(hero, request.num, team)
    if old_hero:
        old_hero.in_team = False
    test_for_gap(team)
    db.commit()
    db.refresh(team)
    return TeamResponse.transform_data(team)


def insert_hero(hero: Optional[UserHero], num: int, team: Team) -> UserHero:
    hero_id = hero.id if hero else None
    if num == 1:
        result = team.hero_1
        team.hero_1_id = hero_id
        return result
    if num == 2:
        result = team.hero_2
        team.hero_2_id = hero_id
        return result
    if num == 3:
        result = team.hero_3
        team.hero_3_id = hero_id
        return result
    if num == 4:
        result = team.hero_4
        team.hero_4_id = hero_id
        return result
    if num == 5:
        result = team.hero_5
        team.hero_5_id = hero_id
        return result
    if num == 6:
        result = team.hero_6
        team.hero_6_id = hero_id
        return result


def get_hero_from_position(num: int, team: Team) -> UserHero:
    if num == 1:
        return team.hero_1
    if num == 2:
        return team.hero_2
    if num == 3:
        return team.hero_3
    if num == 4:
        return team.hero_4
    if num == 5:
        return team.hero_5
    if num == 6:
        return team.hero_6


def switch_heroes(user_id: int, request: TeamRequest, db: Session) -> Team:
    team = team_repo.get_team(user_id, db)
    if team is None:
        raise no_team_object_exception()
    hero: Optional[UserHero] = get_hero_from_position(request.num, team)
    if hero is None:
        raise no_such_hero_exception()
    secondary_hero = insert_hero(hero, request.switch_num, team)
    insert_hero(secondary_hero, request.num, team)
    test_for_gap(team)
    db.commit()
    db.refresh(team)
    return TeamResponse.transform_data(team)


def delete_hero(user_id: int, num: int, db: Session) -> TeamResponse:
    team = team_repo.get_team(user_id, db)
    if team is None:
        raise no_team_object_exception()
    insert_hero(None, num, team)
    move_up(num, team)
    db.commit()
    db.refresh(team)
    return TeamResponse.transform_data(team)


def no_team_object_exception():
    return HTTPException(
        status_code=500,
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


def test_for_gap(team: Team) -> None:
    team_list = [
            team.hero_1_id,
            team.hero_2_id,
            team.hero_3_id,
            team.hero_4_id,
            team.hero_5_id,
            team.hero_6_id
            ]
    initial_gap_ended = False
    for i in reversed(team_list):
        if initial_gap_ended and not i:
            raise gap_in_team_exception()
        if i and not initial_gap_ended:
            initial_gap_ended = True


def move_up(num: int, team: Team) -> None:
    if num < 2:
        team.hero_1_id = team.hero_2_id
    if num < 3:
        team.hero_2_id = team.hero_3_id
    if num < 4:
        team.hero_3_id = team.hero_4_id
    if num < 5:
        team.hero_4_id = team.hero_5_id
    if num < 6:
        team.hero_5_id = team.hero_6_id
    team.hero_6_id = None
