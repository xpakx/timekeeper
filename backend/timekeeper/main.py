from fastapi import FastAPI
from .routers import timer_router
from .db.models import Base
from .db.base import engine

Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(timer_router.router)