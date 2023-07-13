from fastapi import APIRouter, Depends, Query
from .dto import item_schemas
from ..services import reward_service
from typing import Annotated
from ..security.jwt import get_current_user, CurrentUser
from ..db.manager import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/items")


@router.get("/", response_model=list[item_schemas.EquipmentBase])
async def get_timers(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        page: Annotated[int, Query(ge=0)] = 0,
        size: Annotated[int, Query(ge=1, le=20)] = 20,
        db: Session = Depends(get_db)
        ):
    return reward_service.get_items(page, size, user.id, db)
