from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
                      timer_router,
                      user_router,
                      point_router,
                      item_router,
                      hero_router,
                      incubator_router,
                      battle_router
)
from .db.models import Base
from .db.base import engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(timer_router.router)
app.include_router(user_router.router)
app.include_router(point_router.router)
app.include_router(item_router.router)
app.include_router(hero_router.router)
app.include_router(incubator_router.router)
app.include_router(battle_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors(), "body": exc.body},
    )
