from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from ..db.schemas import UserSchema
from ..repository import UserRepository
from ..dependencies import get_db, get_current_user
from ..utils import created_with_location

user_router = APIRouter(prefix="/users")


@user_router.post("/", response_model=UserSchema.User)
def create_user(
    request: Request,
    user: UserSchema.UserCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            db_user = UserRepository.get_user_by_email(db, email=user.email)
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )
            created_user = UserRepository.create_user(db=db, user=user)
            return created_with_location(request, str(created_user.id))
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@user_router.get("/", response_model=list[UserSchema.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            users = UserRepository.get_users(db, skip=skip, limit=limit)
            return users
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@user_router.get("/{user_id}", response_model=UserSchema.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            db_user = UserRepository.get_user(db, user_id=user_id)
            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return db_user
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@user_router.put("/{user_id}")
def update_user(
    user_id: int,
    user: UserSchema.UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if (current_user["role"] == UserSchema.UserRoleEnum.ADMIN) or (
            current_user["role"] == UserSchema.UserRoleEnum.STAFF
            and current_user["id"] == user_id
        ):
            UserRepository.update_user(db, user_id, user)
            return Response(None, status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@user_router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if (current_user["role"] == UserSchema.UserRoleEnum.ADMIN) or (
            current_user["role"] == UserSchema.UserRoleEnum.STAFF
            and current_user["id"] == user_id
        ):
            UserRepository.delete_user(db, user_id)
            return Response(None, status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
