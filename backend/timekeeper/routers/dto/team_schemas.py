from pydantic import BaseModel
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
    num: int
    switch_num: Optional[int]

    class Config:
        orm_mode = True


class TeamResponse(BaseModel):
    heroes: list[UserHeroBase]

    def transform_data(team: Team):
        transformed_data = {
                'heroes': [
                    team.hero_1,
                    team.hero_2,
                    team.hero_3,
                    team.hero_4,
                    team.hero_5,
                    team.hero_6
                    ]
                }
        return TeamResponse(**transformed_data)

    class Config:
        orm_mode = True
