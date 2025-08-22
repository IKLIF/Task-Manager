# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import Base, engine
from .api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
