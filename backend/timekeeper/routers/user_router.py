from fastapi import APIRouter
from .dto import user_schemas
from ..services import user_service

router = APIRouter(prefix="/users")


@router.post("/login", response_model=user_schemas.AuthResponse)
async def logit(request: user_schemas.AuthRequest):
    return user_service.login(request)
