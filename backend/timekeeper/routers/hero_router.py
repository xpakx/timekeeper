from fastapi import APIRouter, Depends, Query
from .dto import hero_schemas
from ..services import hero_service
from typing import Annotated
from ..security.jwt import get_current_user, CurrentUser
from ..db.manager import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/heroes")


@router.get("/", response_model=list[hero_schemas.UserHeroBase])
async def get_heroes(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        page: Annotated[int, Query(ge=0)] = 0,
        size: Annotated[int, Query(ge=1, le=20)] = 20,
        db: Session = Depends(get_db)
        ):
    return hero_service.get_heroes(page, size, user.id, db)


@router.get("/reward", response_model=hero_schemas.HeroBase)
async def generate_hero(
        id: int,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return hero_service.get_hero(id, user.id, db)


@router.get("/crystals", response_model=list[hero_schemas.Crystals])
async def get_crystals(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return {'crystals': hero_service.get_crystals(user.id, db)}
