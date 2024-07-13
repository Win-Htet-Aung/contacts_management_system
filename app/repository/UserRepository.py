from sqlalchemy.orm import Session
from ..db.models import UserModel
from ..db.schemas import UserSchema


def get_user(db: Session, user_id: int):
    return db.query(UserModel.User).filter(UserModel.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel.User).filter(UserModel.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserSchema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = UserModel.User(
        email=user.email, username=user.username, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
