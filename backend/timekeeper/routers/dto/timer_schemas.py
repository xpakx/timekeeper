from pydantic import BaseModel, Field


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
    state: int


class TimerInstance(BaseModel):
    id: int
    start_time: str
    end_time: str
    state: int
    timer_id: int
