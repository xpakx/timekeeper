from pydantic import BaseModel


class TimerRequest(BaseModel):
    name: str
    description: str | None = None
    duration_s: int
