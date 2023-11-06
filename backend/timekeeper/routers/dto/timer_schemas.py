from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from ...db.models import TimerState, TimerDifficulty


class TimerBase(BaseModel):
    name: str
    duration_s: int
    autofinish: bool | None
    rewarded: bool | None
    difficulty: TimerDifficulty | None

    class Config:
        orm_mode = True


class TimerSummary(TimerBase):
    name: str
    description: str | None = None
    duration_s: int


class TimerRequest(BaseModel):
    name: str = Field(strip_whitespace=True, min_length=1)
    description: str | None = None
    duration_s: int = Field(gt=0)
    autofinish: bool | None
    rewarded: bool | None
    difficulty: TimerDifficulty | None

    class Config:
        orm_mode = True

    @validator('name')
    def validate_name_not_empty(cls, name: str):
        new_name = name.strip()
        if len(new_name) == 0:
            raise ValueError("Name cannot be empty")
        return new_name


class TimerResponse(TimerSummary):
    id: int


class StateRequest(BaseModel):
    state: TimerState


class TimerInstance(BaseModel):
    id: int
    start_time: datetime
    reward_time: Optional[int]
    end_time: Optional[datetime]
    state: TimerState
    timer_id: int
    timer: TimerBase

    class Config:
        orm_mode = True


class StateChangeResponse(BaseModel):
    state: TimerState
    points: int
