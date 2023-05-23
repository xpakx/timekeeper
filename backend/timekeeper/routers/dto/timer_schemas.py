from pydantic import BaseModel


class TimerBase(BaseModel):
    name: str
    description: str | None = None
    duration_s: int

    class Config:
        orm_mode = True


class TimerRequest(TimerBase):
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
