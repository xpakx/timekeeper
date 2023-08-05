from pydantic import BaseModel
from .hero_schemas import UserHeroBase


class IncubatorBase(BaseModel):
    id: int
    hero: UserHeroBase
    permanent: bool
    initial_points: int
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
