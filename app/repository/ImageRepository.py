from sqlalchemy.orm import Session
from datetime import datetime
from ..db.models import ImageModel
from ..db.schemas import ImageSchema, UserSchema


def create_image(
    db: Session, image: ImageSchema.ImageCreate, current_user: UserSchema.User
):
    db_image = ImageModel.Image(
        file_url=image.file_url,
        created_by=current_user["id"],
        modified_by=current_user["id"],
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_image(db: Session, image_id: int):
    return db.query(ImageModel.Image).filter(ImageModel.Image.id == image_id).first()


def update_image(
    db: Session,
    image_id: int,
    image: ImageSchema.ImageUpdate,
    current_user: UserSchema.User,
):
    image_update = image.model_dump()
    image_update["modified_by"] = current_user["id"]
    image_update["modified_on"] = datetime.now()
    db.query(ImageModel.Image).filter(ImageModel.Image.id == image_id).update(
        image_update
    )
    db.commit()


def delete_image(db: Session, image_id: int):
    db.query(ImageModel.Image).filter(ImageModel.Image.id == image_id).delete()
    db.commit()
