from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .db.session import SessionLocal
from .db.schemas import UserSchema
from .utils import decode_jwt


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login", scheme_name="Bearer"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema.User | None:
    user = decode_jwt(token)
    return user
