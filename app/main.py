from fastapi import FastAPI
from .db.base import Base
from .db.session import engine
from .routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
