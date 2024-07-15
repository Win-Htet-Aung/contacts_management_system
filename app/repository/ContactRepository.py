from datetime import datetime
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy import select, desc, asc
from ..db.models import ContactModel
from ..db.schemas import ContactSchema, UserSchema


def get_contact(db: Session, contact_id: int):
    return (
        db.query(ContactModel.Contact)
        .filter(ContactModel.Contact.id == contact_id)
        .first()
    )


def get_contacts(
    db: Session,
    page: int,
    size: int,
    sort: str,
    contact_filter: ContactModel.ContactFilter,
):
    sort_func = asc
    if sort.startswith("-"):
        sort = sort[1:]
        sort_func = desc
    pagination_params = Params(page=page, size=size)
    return paginate(
        db,
        contact_filter.filter(select(ContactModel.Contact)).order_by(
            sort_func(ContactModel.Contact.__dict__[sort])
        ),
        pagination_params,
    )


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
