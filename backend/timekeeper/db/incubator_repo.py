from .models import Incubator
from sqlalchemy import and_
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import Session

INCUBATOR = 7


def get_installed(user_id: int, db: Session) -> int:
    return db\
        .query(Incubator)\
        .where(
                and_(
                  Incubator.user_id == user_id,
                  Incubator.broken == false()
                  )
            )\
        .count()


def install_incubator(incubator_id: int, user_id: int, db: Session) -> Incubator:
    entry = Incubator(
            owner_id=user_id,
            broken=False,
            permanent=False,
            )
    db.add(entry)
    db.refresh(entry)
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
