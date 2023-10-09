from pydantic import BaseModel, Field, validator
from ...db.models import ItemRarity, HeroType, MoveCategory
from typing import Optional


class HeroBase(BaseModel):
    id: int
    name: str
    title: Optional[str]
    num: int
    rarity: ItemRarity
    hero_type: Optional[HeroType]
    secondary_hero_type: Optional[HeroType]

    class Config:
        orm_mode = True


class UserHeroBase(BaseModel):
    id: int
    incubated: bool

    class Config:
        orm_mode = True


class UserHeroMin(UserHeroBase):
    hero: HeroBase


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
    move_type: Optional[HeroType]
    move_category: Optional[MoveCategory]

    class Config:
        orm_mode = True


class SkillSetBase(BaseModel):
    skill_1: Optional[SkillBase]
    skill_2: Optional[SkillBase]
    skill_3: Optional[SkillBase]
    skill_4: Optional[SkillBase]

    class Config:
        orm_mode = True


class HeroDetails(HeroBase):
    health: int
    title: str
    description: str
    base_hp: int
    base_attack: int
    base_defense: int
    base_speed: int
    base_special_defense: int
    base_special_attack: int


class UserHeroDetails(UserHeroBase):
    damage: int
    skillset: SkillSetBase
    hero: HeroDetails

    @validator('skillset')
    def convert_skills(cls, skillset: SkillSetBase):
        return [skillset.skill_1,
                skillset.skill_2,
                skillset.skill_3,
                skillset.skill_4]
