from fastapi import APIRouter, Depends
from .dto import hero_schemas, incubator_schemas
from ..services import incubator_service
from typing import Annotated
from ..security.jwt import get_current_user, CurrentUser
from ..db.manager import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/incubators")


@router.get("/", response_model=list[incubator_schemas.IncubatorBase])
async def get_heroes(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return incubator_service.get_incubators(user.id, db)


@router.post("/", response_model=list[incubator_schemas.IncubatorBase])
async def install_incubator(
        request: incubator_schemas.InstallRequest,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return incubator_service.install_incubator(user.id, request.item_id, db)


@router.post(
        "/{incubator_id}",
        response_model=list[incubator_schemas.IncubatorBase])
async def insert_hero(
        incubator_id: int,
        request: incubator_schemas.IncubationRequest,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return incubator_service.insert_hero(
            user.id,
            request.hero_id,
            incubator_id,
            db)


@router.post(
        "/{incubator_id}/hero",
        response_model=list[hero_schemas.UserHeroBase])
async def get_hero(
        incubator_id: int,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return incubator_service.get_hero(user.id, incubator_id, db)


@router.delete("/{incubator_id}")
async def delete_incubator(
        incubator_id: int,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return incubator_service.delete_incubator(user.id, incubator_id, db)
