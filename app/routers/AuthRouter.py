from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.schemas import JwtSchema
from ..dependencies import get_db
from ..services import AuthService

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=JwtSchema.Jwt)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService.login(form_data, db)


# @contact_router.get("/logout", response_model=list[ContactSchema.Contact])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     contacts = ContactRepository.get_contacts(db, skip=skip, limit=limit)
#     return contacts
