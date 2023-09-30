from pydantic import BaseModel
from .hero_schemas import UserHeroMin
from typing import Optional


class IncubatorBase(BaseModel):
    id: int
    hero: Optional[UserHeroMin]
    permanent: bool
    initial_points: Optional[int]
    usages: int

    class Config:
        orm_mode = True


class IncubationRequest(BaseModel):
    hero_id: int

    class Config:
        orm_mode = True


class InstallRequest(BaseModel):
    item_id: int

    class Config:
        orm_mode = True
