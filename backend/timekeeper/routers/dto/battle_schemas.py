from pydantic import BaseModel, root_validator
from typing import Optional
from .hero_schemas import UserHeroBase, HeroBase, SkillSetBase
import enum


class HeroBattle(HeroBase):
    base_hp: int


class UserHeroBattle(UserHeroBase):
    hp: int
    damage: int
    hero: HeroBattle
    skillset: SkillSetBase


class EnemyHeroBattle(UserHeroBase):
    damage: int
    hero: HeroBase


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
