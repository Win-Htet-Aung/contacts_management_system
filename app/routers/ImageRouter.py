from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
)
from sqlalchemy.orm import Session
from ..db.schemas import UserSchema
from ..dependencies import get_db, get_current_user
from ..services import ImageService

image_router = APIRouter(prefix="/images")


@image_router.get("/{image_id}")
def get_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [
            UserSchema.UserRoleEnum.ADMIN,
            UserSchema.UserRoleEnum.STAFF,
        ]:
            return ImageService.get_image(db, image_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@image_router.delete("/{image_id}")
def delete_imge(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [
            UserSchema.UserRoleEnum.ADMIN,
            UserSchema.UserRoleEnum.STAFF,
        ]:
            ImageService.delete_image(db, image_id)
            return Response(None, status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
