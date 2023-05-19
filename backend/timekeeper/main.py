from fastapi import FastAPI
from .routers import timer_router


app = FastAPI()
app.include_router(timer_router.router)
