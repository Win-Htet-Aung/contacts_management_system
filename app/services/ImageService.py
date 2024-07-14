import os
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from ..db.models import ContactModel
from ..db.schemas import UserSchema, ImageSchema
from ..repository import ImageRepository


def create_image(
    db: Session,
    current_user: UserSchema.User,
    image: UploadFile,
    contact: ContactModel.Contact,
):
    ext = image.filename.split(".")[-1]
    model_name = contact.get_model_name()
    obj_id = str(contact.id)
    filename = f"app/static/img/{model_name}-{obj_id}.{ext}"
    with open(filename, "wb") as f:
        f.write(image.file.read())
    file_url = filename.split("/", 1)[1]
    image_create = ImageSchema.ImageCreate(file_url=file_url)
    created_image = ImageRepository.create_image(db, image_create, current_user)
    return created_image


def get_image(db: Session, image_id: int):
    db_image = ImageRepository.get_image(db, image_id)
    if db_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_image


def update_image(
    db: Session,
    current_user: UserSchema.User,
    image_id: int,
    image: UploadFile,
):
    ext = image.filename.split(".")[-1]
    db_image = get_image(db, image_id)
    old_filename = f"app/{db_image.file_url}"
    os.remove(old_filename)
    filename = f"app/{db_image.file_url}".split(".")[0] + f".{ext}"
    with open(filename, "wb") as f:
        f.write(image.file.read())
    file_url = filename.split("/", 1)[1]
    image_update = ImageSchema.ImageUpdate(file_url=file_url)
    ImageRepository.update_image(db, image_id, image_update, current_user)


def delete_image(db: Session, image_id: int):
    db_image = get_image(db, image_id)
    if db_image:
        filename = f"app/{db_image.file_url}"
        os.remove(filename)
        ImageRepository.delete_image(db, image_id)
