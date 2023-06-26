from pydantic import BaseModel


class PointsBase(BaseModel):
    points: int

    class Config:
        orm_mode = True


class PointsResponse(PointsBase):
    pass
