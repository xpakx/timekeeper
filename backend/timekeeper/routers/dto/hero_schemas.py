from pydantic import BaseModel
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
    item_id: int
    num: int

    class Config:
        orm_mode = True
