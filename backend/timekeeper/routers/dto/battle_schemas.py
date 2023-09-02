from pydantic import BaseModel
from typing import Optional
from .hero_schemas import UserHeroBase
import enum


class BattleBase(BaseModel):
    id: int
    finished: bool
    hero: Optional[UserHeroBase]
    enemy: Optional[UserHeroBase]

    class Config:
        orm_mode = True


class NewBattleRequest(BaseModel):
    id: int


class MoveType(enum.Enum):
    flee = "flee"
    skill = "skill"
    item = "item"


class MoveRequest(BaseModel):
    id: int
    move: MoveType
