from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from ..db.schemas import ContactSchema, UserSchema, HistorySchema
from ..repository import ContactRepository
from . import ImageService, HistoryService


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
            ContactSchema.ContactUpdate(**created_contact.__dict__).model_dump(),
            current_user,
        )
    history_create = HistorySchema.HistoryCreate(
        object_type="Contact",
        object_name=f"Contact-{created_contact.id}",
        activity=HistorySchema.ActivityEnum.CREATE,
    )
    payload = ContactSchema.ContactCreate(**created_contact.__dict__).model_dump()
    HistoryService.create_history(
        db, history_create, created_contact.id, payload, current_user
    )
    return created_contact


def get_contact(db: Session, contact_id: int):
    db_contact = ContactRepository.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_contact


def update_contact(
    db: Session,
    contact_id: int,
    contact: ContactSchema.ContactUpdate,
    image: UploadFile | None,
    current_user: UserSchema.User,
):
    db_contact = get_contact(db, contact_id)
    update_data = contact.model_dump()
    if image:
        if db_contact.image_id:
            ImageService.update_image(db, current_user, db_contact.image_id, image)
            update_data["image_id"] = db_contact.image_id
        else:
            created_image = ImageService.create_image(
                db, current_user, image, db_contact
            )
            update_data["image_id"] = created_image.id
    else:
        if db_contact.image_id:
            ImageService.delete_image(db, db_contact.image_id)
    ContactRepository.update_contact(db, contact_id, update_data, current_user)
    history_create = HistorySchema.HistoryCreate(
        object_type="Contact",
        object_name=f"Contact-{db_contact.id}",
        activity=HistorySchema.ActivityEnum.UPDATE,
    )
    payload = update_data
    HistoryService.create_history(
        db, history_create, db_contact.id, payload, current_user
    )


def delete_contact(db: Session, contact_id: int, current_user: UserSchema.User):
    db_contact = get_contact(db, contact_id)
    if db_contact.image_id:
        ImageService.delete_image(db, db_contact.image_id)
    history_create = HistorySchema.HistoryCreate(
        object_type="Contact",
        object_name=f"Contact-{db_contact.id}",
        activity=HistorySchema.ActivityEnum.DELETE,
    )
    payload = {}
    HistoryService.create_history(
        db, history_create, db_contact.id, payload, current_user
    )
    ContactRepository.delete_contact(db, contact_id)
