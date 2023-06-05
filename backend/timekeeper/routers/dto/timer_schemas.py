from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ...db.models import TimerState


class TimerBase(BaseModel):
    name: str
    description: str | None = None
    duration_s: int

    class Config:
        orm_mode = True


class TimerRequest(BaseModel):
    name: str = Field(strip_whitespace=True, min_length=1)
    description: str | None = None
    duration_s: int = Field(gt=0)

    class Config:
        orm_mode = True
    pass


class TimerResponse(TimerBase):
    id: int


class StateRequest(BaseModel):
    state: TimerState


class TimerInstance(BaseModel):
    id: int
    start_time: datetime
    end_time: Optional[datetime]
    state: TimerState
    timer_id: int

    class Config:
        orm_mode = True
