from .models import Incubator
from sqlalchemy import and_
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import Session
from typing import Optional


def get_installed(user_id: int, db: Session) -> int:
    return db\
        .query(Incubator)\
        .where(
                and_(
                  Incubator.owner_id == user_id,
                  Incubator.broken == false()
                  )
            )\
        .count()


def install_incubator(
        incubator_id: int,
        usages: int,
        user_id: int,
        db: Session) -> Incubator:
    entry = Incubator(
            owner_id=user_id,
            broken=False,
            permanent=False,
            usages=usages
            )
    db.add(entry)
    return entry


def get_incubators(user_id: int, db: Session):
    return db\
        .query(Incubator)\
        .where(
                    and_(
                        Incubator.owner_id == user_id,
                        Incubator.broken == false()
                        )
                    )\
        .all()


def get_incubator(
        user_id: int,
        hero_id: int,
        db: Session) -> Optional[Incubator]:
    return db\
        .query(Incubator)\
        .where(
                    and_(
                        Incubator.owner_id == user_id,
                        Incubator.id == hero_id,
                        Incubator.broken == false()
                        )
                    )\
        .first()
