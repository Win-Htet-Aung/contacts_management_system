from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.schemas import UserSchema
from ..repository import UserRepository
from ..dependencies import get_db, get_current_user

user_router = APIRouter(prefix="/users")


@user_router.post("/", response_model=UserSchema.User)
def create_user(
    user: UserSchema.UserCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        db_user = UserRepository.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return UserRepository.create_user(db=db, user=user)
    else:
        raise HTTPException(status_code=401)


@user_router.get("/", response_model=list[UserSchema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = UserRepository.get_users(db, skip=skip, limit=limit)
    return users


@user_router.get("/{user_id}", response_model=UserSchema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserRepository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
