from pydantic import BaseModel, Field, root_validator
from typing import Optional
import enum
from .hero_schemas import UserHeroMin
from ...db.models import Team


class TeamAction(enum.Enum):
    add = "add"
    switch = "switch"
    delete = "delete"


class TeamRequest(BaseModel):
    hero_id: Optional[int]
    action: TeamAction
    num: int = Field(gt=0, le=4)
    switch_num: Optional[int] = Field(gt=0, le=4)

    @root_validator()
    def validate_switch_num(cls, values):
        action = values.get('action')
        value = values.get('switch_num')
        if action == TeamAction.switch and value is None:
            raise ValueError("Position to switch cannot be empty")
        return values

    @root_validator()
    def validate_hero_id(cls, values):
        action = values.get('action')
        value = values.get('hero_id')
        if action == TeamAction.add and value is None:
            raise ValueError("Hero id cannot be empty")
        return values


class TeamResponse(BaseModel):
    heroes: list[UserHeroMin]

    def transform_data(team: Team):
        transformed_data = {
                'heroes': []
                }
        if team.hero_1:
            transformed_data['heroes'].append(team.hero_1)
        if team.hero_2:
            transformed_data['heroes'].append(team.hero_2)
        if team.hero_3:
            transformed_data['heroes'].append(team.hero_3)
        if team.hero_4:
            transformed_data['heroes'].append(team.hero_4)
        if team.hero_5:
            transformed_data['heroes'].append(team.hero_5)
        if team.hero_6:
            transformed_data['heroes'].append(team.hero_6)
        return TeamResponse(**transformed_data)

    class Config:
        orm_mode = True
