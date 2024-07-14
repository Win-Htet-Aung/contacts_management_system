from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
    Request,
    UploadFile,
)
from sqlalchemy.orm import Session
from ..db.schemas import ImageSchema, UserSchema
from ..dependencies import get_db, get_current_user
from ..utils import created_with_location

image_router = APIRouter(prefix="/images")


@image_router.post("/")
def upload_image(
    request: Request,
    image: UploadFile,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    pass
