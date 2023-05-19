from fastapi import APIRouter

router = APIRouter(prefix="/timers")


@router.get("/")
async def add_timer():
    return {"test": "timer path"}
