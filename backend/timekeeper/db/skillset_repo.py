from .models import SkillSet
from sqlalchemy.orm import Session


def create_entry(hero, db: Session):
    entry = SkillSet(
            hero=hero,
            )
    db.add(entry)
