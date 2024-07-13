from sqlalchemy.orm import Session
from ..db.models import UserModel
from ..db.schemas import UserSchema
from ..utils import get_hashed_password


def get_user(db: Session, user_id: int):
    return db.query(UserModel.User).filter(UserModel.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel.User).filter(UserModel.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> UserModel.User | None:
    return db.query(UserModel.User).filter(UserModel.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserSchema.UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = UserModel.User(
        email=user.email, username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
