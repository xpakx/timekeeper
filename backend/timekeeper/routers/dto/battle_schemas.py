from pydantic import BaseModel, root_validator, validator
from typing import Optional
from .hero_schemas import UserHeroBase, HeroBase, SkillSetBase
import enum
from ...services.mechanics.battle_mech_service import calculate_hp_
import math


class HeroBattle(HeroBase):
    base_hp: int


class UserHeroBattle(UserHeroBase):
    hp: int
    damage: int
    hero: HeroBattle
    skillset: SkillSetBase
    level: int

    @validator('skillset')
    def convert_skills(cls, skillset: SkillSetBase):
        return [skillset.skill_1,
                skillset.skill_2,
                skillset.skill_3,
                skillset.skill_4]

    @root_validator()
    def transform_data(cls, values):
        damage = values.get('damage')
        hp = values.get('hp')
        hero = values.get('hero')
        hp = calculate_hp_(hero.base_hp, hp, values.get('level'))
        hero.base_hp = None
        values['current_hp'] = math.floor(100*((hp-damage))/hp)
        values['hp'] = hp
        return values


class EnemyHeroBattle(UserHeroBase):
    hp: int
    damage: int
    hero: HeroBattle
    level: int

    @root_validator()
    def transform_data(cls, values):
        damage = values.pop('damage')
        hp = values.pop('hp')
        hero = values.get('hero')
        hp = calculate_hp_(hero.base_hp, hp, values.get('level'))
        hero.base_hp = None
        values['current_hp'] = math.floor(100*((hp-damage))/hp)
        return values


class BattleBase(BaseModel):
    id: int
    finished: bool
    hero: Optional[UserHeroBattle]
    enemy: Optional[EnemyHeroBattle]

    class Config:
        orm_mode = True


class NewBattleRequest(BaseModel):
    id: int


class MoveType(enum.Enum):
    flee = "flee"
    skill = "skill"
    item = "item"


class MoveRequest(BaseModel):
    id: Optional[int]
    move: MoveType

    @root_validator()
    def validate_switch_num(cls, values):
        move = values.get('move')
        value = values.get('id')
        if move in [MoveType.skill, MoveType.item] and value is None:
            raise ValueError("Id cannot be empty")
        return values
