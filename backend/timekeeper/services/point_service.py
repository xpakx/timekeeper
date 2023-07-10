from ..db import point_repo
from ..db.models import Points
from sqlalchemy.orm import Session


def get_points(user_id: int, db: Session) -> Points:
    return point_repo.get_points(user_id, db)
