from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..db.schemas import UserSchema, JwtSchema
from ..repository import UserRepository
from ..utils import verify_password, sign_jwt


def login(user: UserSchema.UserLogin, db: Session) -> JwtSchema.Jwt:
    db_user = UserRepository.get_user_by_username(db, user.username)
    if db_user:
        if verify_password(user.password, db_user.hashed_password):
            token = sign_jwt(UserSchema.User(**db_user.__dict__))
            return JwtSchema.Jwt(token=token)
        else:
            raise HTTPException(status_code=400, detail="Invalid Credentials!")
    else:
        raise HTTPException(status_code=400, detail="Ivalid Credentials!")
