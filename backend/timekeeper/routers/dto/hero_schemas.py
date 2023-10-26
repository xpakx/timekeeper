from pydantic import BaseModel, Field, validator, root_validator
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
    item_id: Optional[int] = Field(gt=0)
    skill_id: Optional[int] = Field(gt=0)
    num: int = Field(gt=0, le=4)

    @root_validator()
    def validate_at_least_one_id_value(cls, values):
        item = values.get('item_id')
        skill = values.get('skill_id')
        if (not item) and (not skill):
            raise ValueError("Id cannot be empty")
        if item and skill:
            raise ValueError("Cannot use two ids")
        return values


class SkillBase(BaseModel):
    id: int
    name: str
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


class EvolveRequest(BaseModel):
    hero_id: int
    item_id: Optional[int]
