from sqlalchemy.orm import Session
from ..db.models import ContactModel
from ..db.schemas import ContactSchema


# def get_user(db: Session, user_id: int):
#     return db.query(UserModel.User).filter(UserModel.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(UserModel.User).filter(UserModel.User.email == email).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ContactModel.Contact).offset(skip).limit(limit).all()


def create_contact(db: Session, contact: ContactSchema.ContactCreate):
    db_contact = ContactModel.Contact(
        **contact.model_dump()
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
