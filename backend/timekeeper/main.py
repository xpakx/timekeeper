from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .routers import timer_router, user_router
from .db.models import Base
from .db.base import engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(timer_router.router)
app.include_router(user_router.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors(), "body": exc.body},
    )
