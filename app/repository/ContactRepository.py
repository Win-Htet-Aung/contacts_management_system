from datetime import datetime
from sqlalchemy.orm import Session
from ..db.models import ContactModel
from ..db.schemas import ContactSchema, UserSchema


def get_contact(db: Session, contact_id: int):
    return (
        db.query(ContactModel.Contact)
        .filter(ContactModel.Contact.id == contact_id)
        .first()
    )


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ContactModel.Contact).offset(skip).limit(limit).all()


def create_contact(
    db: Session, contact: ContactSchema.ContactCreate, current_user: UserSchema.User
):
    db_contact = ContactModel.Contact(**contact.model_dump())
    db_contact.created_by = current_user["id"]
    db_contact.modified_by = current_user["id"]
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(
    db: Session,
    contact_id: int,
    contact: dict,
    current_user: UserSchema.User,
):
    contact["modified_by"] = current_user["id"]
    contact["modified_on"] = datetime.now()
    db.query(ContactModel.Contact).filter(ContactModel.Contact.id == contact_id).update(
        contact
    )
    db.commit()


def delete_contact(db: Session, contact_id: int):
    db.query(ContactModel.Contact).filter(
        ContactModel.Contact.id == contact_id
    ).delete()
    db.commit()
