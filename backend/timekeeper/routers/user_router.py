from fastapi import APIRouter, Depends
from .dto import user_schemas
from ..services import user_service
from sqlalchemy.orm import Session
from ..db.manager import get_db
from typing import Optional

router = APIRouter(prefix="/users")


@router.post("/login", response_model=user_schemas.AuthResponse)
async def login(request: user_schemas.AuthRequest,
                db: Session = Depends(get_db)
                ):
    return user_service.login(request, db)


@router.post("/register", response_model=user_schemas.AuthResponse)
async def register(request: user_schemas.RegistrationRequest,
                   db: Session = Depends(get_db)
                   ):
    return user_service.register(request, db)
