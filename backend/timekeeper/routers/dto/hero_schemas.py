from pydantic import BaseModel, Field
from ...db.models import ItemRarity
from typing import Optional


class HeroBase(BaseModel):
    id: int
    name: str
    title: Optional[str]
    num: int
    rarity: ItemRarity

    class Config:
        orm_mode = True


class UserHeroBase(BaseModel):
    id: int
    hero: HeroBase
    incubated: bool

    class Config:
        orm_mode = True


class Crystals(BaseModel):
    crystals: int


class SkillRequest(BaseModel):
    item_id: int = Field(gt=0)
    num: int = Field(gt=0, le=4)


class SkillBase(BaseModel):
    id: int
    priority: int
    accuracy: int
    power: int
    max_usages: int

    class Config:
        orm_mode = True


class SkillSetBase(BaseModel):
    skill_1: Optional[SkillBase]
    skill_2: Optional[SkillBase]
    skill_3: Optional[SkillBase]
    skill_4: Optional[SkillBase]

    class Config:
        orm_mode = True


class UserHeroDetails(HeroBase):
    skillset: SkillSetBase
