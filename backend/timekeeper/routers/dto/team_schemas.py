from pydantic import BaseModel, Field
from typing import Optional
import enum
from .hero_schemas import UserHeroBase
from ...db.models import Team


class TeamAction(enum.Enum):
    add = "add"
    switch = "switch"


class TeamRequest(BaseModel):
    hero_id: int
    action: TeamAction
    num: int = Field(gt=0, le=4)
    switch_num: Optional[int] = Field(gt=0, le=4)


class TeamResponse(BaseModel):
    heroes: list[UserHeroBase]

    def transform_data(team: Team):
        transformed_data = {
                'heroes': []
                }
        if team.hero_1:
            transformed_data['heroes'].push(team.hero1)
        if team.hero_2:
            transformed_data['heroes'].push(team.hero2)
        if team.hero_3:
            transformed_data['heroes'].push(team.hero3)
        if team.hero_4:
            transformed_data['heroes'].push(team.hero4)
        if team.hero_5:
            transformed_data['heroes'].push(team.hero5)
        if team.hero_6:
            transformed_data['heroes'].push(team.hero6)
        return TeamResponse(**transformed_data)

    class Config:
        orm_mode = True
