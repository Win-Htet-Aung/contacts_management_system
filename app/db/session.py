from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import settings


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://postgres:{settings.db_password}@localhost/postgres"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
