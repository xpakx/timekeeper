from pydantic import BaseModel
from ...db.models import ItemRarity
from typing import Optional


class HeroBase(BaseModel):
    id: int
    name: str
    title: str
    num: int
    rarity: ItemRarity

    class Config:
        orm_mode = True


class UserHeroBase(BaseModel):
    id: int
    hero: HeroBase
    incubated: Optional[bool]  # TODO: delete optional, it's temporary for legacy test db

    class Config:
        orm_mode = True


class Crystals(BaseModel):
    crystals: int
