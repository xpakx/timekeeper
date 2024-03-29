from fastapi import APIRouter, Depends, Query
from .dto import hero_schemas
from ..services import hero_service, skill_service
from typing import Annotated
from ..security.jwt import get_current_user, CurrentUser
from ..db.manager import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/heroes")


@router.get("/", response_model=list[hero_schemas.UserHeroMin])
async def get_heroes(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        page: Annotated[int, Query(ge=0)] = 0,
        size: Annotated[int, Query(ge=1, le=20)] = 20,
        db: Session = Depends(get_db)
        ):
    return hero_service.get_heroes(page, size, user.id, db)


@router.post("/reward", response_model=hero_schemas.HeroBase)
async def generate_hero(
        request: hero_schemas.HeroGenerateRequest,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    starter = request.starter if request.starter else False
    return hero_service.get_hero(user.id, starter, db)


@router.get("/crystals", response_model=hero_schemas.Crystals)
async def get_crystals(
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return {'crystals': hero_service.get_crystals(user.id, db)}


@router.post("/{id}/skills", response_model=hero_schemas.UserHeroMin)
async def teach_skill(
        request: hero_schemas.SkillRequest,
        id: int,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return skill_service.teach_hero(
            user.id,
            id,
            request.item_id,
            request.skill_id,
            request.num,
            db
            )


@router.get("/{id}", response_model=hero_schemas.UserHeroDetails)
async def get_hero(
        id: int,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return hero_service.get_user_hero(user.id, id, db)


@router.post("/{id}/evolve", response_model=hero_schemas.UserHeroMin)
async def evolve_hero(
        request: hero_schemas.EvolveRequest,
        id: int,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return hero_service.evolve_user_hero(
            user.id,
            id,
            request.hero_id,
            request.item_id,
            db
            )


@router.get("/{id}/skills/learnable",
            response_model=list[hero_schemas.SkillBase])
async def get_learnable_skills(
        id: int,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return skill_service.get_learnable_skills(user.id, id, db)


@router.get("/{id}/evolve", response_model=list[hero_schemas.EvolvingOption])
def get_evolving_options(
        id: int,
        user: Annotated[CurrentUser, Depends(get_current_user)],
        db: Session = Depends(get_db)
        ):
    return hero_service.get_evolving_options(user.id, id, db)
