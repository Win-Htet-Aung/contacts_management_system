from sqlalchemy.orm import Session
from fastapi import UploadFile
from ..db.schemas import ContactSchema, UserSchema
from ..repository import ContactRepository
from . import ImageService


def create_contact(
    db: Session,
    contact: ContactSchema.ContactCreate,
    image: UploadFile,
    current_user: UserSchema.User,
):
    created_contact = ContactRepository.create_contact(db, contact, current_user)
    if image:
        created_image = ImageService.create_image(
            db, current_user, image, created_contact
        )
        created_contact.image_id = created_image.id
        ContactRepository.update_contact(
            db,
            created_contact.id,
            ContactSchema.ContactUpdate(**created_contact.__dict__),
            current_user,
        )
    return created_contact


def get_contact(db: Session, contact_id: int):
    return ContactRepository.get_contact(db, contact_id)


def update_contact(
    db: Session,
    contact_id: int,
    contact: ContactSchema.ContactUpdate,
    image: UploadFile,
    current_user: UserSchema.User,
):
    db_contact = get_contact(db, contact_id)
    update_data = {k: v for k, v in contact.model_dump().items() if v is not None}
    if image:
        if db_contact.image_id:
            ImageService.update_image(db, current_user, db_contact.image_id, image)
        else:
            created_image = ImageService.create_image(
                db, current_user, image, db_contact
            )
            update_data["image_id"] = created_image.id
    ContactRepository.update_contact(db, contact_id, update_data, current_user)


def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact.image_id:
        ImageService.delete_image()
    ContactRepository.delete_contact(db, contact_id)
