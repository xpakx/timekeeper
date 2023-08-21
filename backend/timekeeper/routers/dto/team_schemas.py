from pydantic import BaseModel
from typing import Optional
import enum


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
