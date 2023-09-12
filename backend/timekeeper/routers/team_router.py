from fastapi import APIRouter, Depends
from .dto import team_schemas
from ..services import team_service
from typing import Annotated
from ..security.jwt import get_current_user, CurrentUser
from ..db.manager import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/teams")


@router.post("/", response_model=team_schemas.TeamResponse)
async def change_team(
        request: team_schemas.TeamRequest,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return team_service.change_team(user.id, request, db)


@router.get("/", response_model=team_schemas.TeamResponse)
async def get_team(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return team_service.get_team(user.id, db)
