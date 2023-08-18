from .models import SkillSet, Skill
from sqlalchemy.orm import Session


def create_entry(hero, db: Session):
    entry = SkillSet(
            hero=hero,
            )
    db.add(entry)


def teach_skill(hero_id: int, skill_id: int, num: int, db: Session):
    entry: SkillSet = db\
        .query(SkillSet)\
        .where(SkillSet.hero_id == hero_id)\
        .first()
    if not entry:
        pass
    if num == 1:
        entry.skill_1_id = skill_id
    elif num == 2:
        entry.skill_2_id = skill_id
    elif num == 3:
        entry.skill_3_id = skill_id
    elif num == 4:
        entry.skill_4_id = skill_id
    db.commit()


def get_skill(item_id: int, db: Session):
    return db\
        .query(Skill)\
        .where(Skill.item_id == item_id)\
        .first()
