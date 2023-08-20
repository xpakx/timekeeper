from .models import Team
from sqlalchemy.orm import Session
from typing import Optional


def create_team(user_id: int, db: Session) -> Team:
    team = Team(
            user_id=user_id,
            )
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def get_team(user_id: int, db: Session) -> Optional[Team]:
    return db\
        .query(Team)\
        .where(
             Team.user_id == user_id,
            )\
        .first()
