from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.schemas import ContactSchema
from ..repository import ContactRepository
from ..dependencies import get_db

contact_router = APIRouter(prefix="/contacts")


@contact_router.post("/", response_model=ContactSchema.Contact)
def create_contact(contact: ContactSchema.ContactCreate, db: Session = Depends(get_db)):
    return ContactRepository.create_contact(db=db, contact=contact)


@contact_router.get("/", response_model=list[ContactSchema.Contact])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = ContactRepository.get_contacts(db, skip=skip, limit=limit)
    return contacts


# @user_router.get("/users/{user_id}", response_model=UserSchema.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = UserRepository.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
