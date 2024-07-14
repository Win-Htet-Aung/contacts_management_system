from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .db.base import Base
from .db.session import engine
from .routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
