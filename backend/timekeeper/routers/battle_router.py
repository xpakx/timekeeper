from fastapi import APIRouter, Depends
from .dto import battle_schemas
from ..services import battle_service
from typing import Annotated
from ..security.jwt import get_current_user, CurrentUser
from ..db.manager import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/battles")


@router.get("/", response_model=battle_schemas.BattleBase)
async def get_current_battle(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return battle_service.get_current_battle(user.id, db)


@router.post("/", response_model=battle_schemas.BattleBase)
async def create_battle(
        request: battle_schemas.NewBattleRequest,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return battle_service.create_battle(user.id, request.id, db)


@router.get("/{id}", response_model=battle_schemas.BattleBase)
async def get_battle(
        id: int,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return battle_service.get_battle(user.id, id, db)
