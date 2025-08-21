# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import Base, engine
from .api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # создаем таблицы
    yield  # здесь можно будет делать shutdown-процедуры

app = FastAPI(lifespan=lifespan)
app.include_router(router)
