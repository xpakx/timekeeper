from ..db import point_repo
from ..db.models import Points
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_points(user_id: int, db: Session) -> Points:
    points = point_repo.get_points(user_id, db)
    if points is None:
        raise no_points_object_exception()
    return points


def no_points_object_exception():
    return HTTPException(
        status_code=500,
        detail="Points not initialized for user!",
    )
