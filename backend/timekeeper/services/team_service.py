from ..db import team_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.models import Team


def get_team(user_id: int, db: Session) -> Team:
    team = team_repo.get_team(user_id, db)
    if team is None:
        raise no_team_object_exception()
    return team


def no_team_object_exception():
    return HTTPException(
        status_code=500,
        detail="No team object!",
    )
