from ..routers.dto.timer_schemas import TimerRequest
from .models import Points
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from sqlalchemy import and_
from sqlalchemy.sql import func


def create_points(user_id: int, db: Session):
    new_points = Points(
            points=0,
            owner_id=user_id,
            )
    db.add(new_points)
    db.commit()
    db.refresh(new_points)
    return new_points


def get_points(user_id: int, db: Session):
    return db\
        .query(Points)\
        .where(
              Points.owner_id == user_id
            )\
        .first()


def add_points(points: int, user_id: int, db: Session):
    db_points = db\
        .query(points)\
        .where(
              points.owner_id == user_id
            )\
        .first()
    if not db_points:
        return
    db_points.points += points
    db.commit()
    db.refresh(db_points)
    return db_points
