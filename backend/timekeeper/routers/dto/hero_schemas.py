from pydantic import BaseModel
from ...db.models import ItemRarity


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

    class Config:
        orm_mode = True


class Crystals(BaseModel):
    crystals: int
