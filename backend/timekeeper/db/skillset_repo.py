from .models import SkillSet, Skill, SkillHero
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException
from typing import Optional


def create_entry(hero, db: Session) -> None:
    entry = SkillSet(
            hero=hero,
            usages_1=0,
            usages_2=0,
            usages_3=0,
            usages_4=0
            )
    db.add(entry)


def teach_skill(hero_id: int, skill_id: int, num: int, db: Session) -> None:
    entry: SkillSet = db\
        .query(SkillSet)\
        .where(SkillSet.hero_id == hero_id)\
        .first()
    if not entry:
        raise not_initialized_exception()
    if num == 1:
        entry.skill_1_id = skill_id
    elif num == 2:
        entry.skill_2_id = skill_id
    elif num == 3:
        entry.skill_3_id = skill_id
    elif num == 4:
        entry.skill_4_id = skill_id
    db.commit()


def get_skill(item_id: int, db: Session) -> Optional[Skill]:
    return db\
        .query(Skill)\
        .where(Skill.item_id == item_id)\
        .first()


def get_skill_by_id(skill_id: int, db: Session) -> Optional[Skill]:
    return db\
        .query(Skill)\
        .where(Skill.id == skill_id)\
        .first()


def test_skill(hero_id: int, skill_id: int, db: Session) -> bool:
    entry: SkillHero = db\
        .query(SkillHero)\
        .where(
                and_(SkillHero.hero_id == hero_id,
                     SkillHero.skill_id == skill_id)
                )\
        .first()
    if entry:
        return True
    return False


def test_skill_at_level(
        hero_id: int,
        skill_id: int,
        level: int,
        db: Session) -> bool:
    entry: SkillHero = db\
        .query(SkillHero)\
        .where(
                and_(SkillHero.hero_id == hero_id,
                     SkillHero.skill_id == skill_id,
                     SkillHero.level == level)
                )\
        .first()
    if entry:
        return True
    return False


def not_initialized_exception():
    return HTTPException(
        status_code=500,
        detail="Skillset not initialized",
    )


def get_skills(hero_id: int, level: int,  db: Session) -> list[Skill]:
    return db\
        .query(SkillHero)\
        .join(Skill, SkillHero.skill)\
        .where(
             and_(
                 SkillHero.hero_id == hero_id,
                 SkillHero.level == level
                 )
            ).all()
