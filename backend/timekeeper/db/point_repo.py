from .models import Points
from sqlalchemy.orm import Session
from typing import Optional


def create_points(user_id: int, db: Session) -> Points:
    new_points = Points(
            points=0,
            user_id=user_id,
            )
    db.add(new_points)
    db.commit()
    db.refresh(new_points)
    return new_points


def get_points(user_id: int, db: Session) -> Optional[Points]:
    return db\
        .query(Points)\
        .where(
              Points.user_id == user_id
            )\
        .first()


def add_points(points: int, user_id: int, db: Session) -> Points:
    db_points = db\
        .query(Points)\
        .where(
              Points.user_id == user_id
            )\
        .first()
    if not db_points:
        new_points = Points(
            points=points,
            user_id=user_id,
            )
        db.add(new_points)
        db.commit()
        db.refresh(new_points)
        return new_points
    db_points.points += points
    db.commit()
    db.refresh(db_points)
    return db_points
