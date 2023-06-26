from fastapi import APIRouter, Depends
from .dto import point_schemas
from ..services import point_service
from typing import Annotated
from ..security.jwt import get_current_user, CurrentUser
from ..db.manager import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/points")


@router.get("/", response_model=list[point_schemas.PointsResponse])
async def get_points(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return point_service.get_points(user.id, db)
