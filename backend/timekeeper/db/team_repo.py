from .models import Team
from sqlalchemy.orm import Session


def create_team(user_id: int, db: Session):
    team = Team(
            user_id=user_id,
            )
    db.add(team)
    db.commit()
    db.refresh(team)
    return team
