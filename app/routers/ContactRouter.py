from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
    UploadFile,
    Response,
)
from sqlalchemy.orm import Session
from pyfa_converter_v2 import FormDepends
from fastapi_pagination import Page
from fastapi_filter import FilterDepends
from ..db.schemas import ContactSchema, UserSchema
from ..db.models import ContactModel
from ..repository import ContactRepository
from ..services import ContactService
from ..dependencies import get_db, get_current_user
from ..utils import created_with_location

contact_router = APIRouter(prefix="/contacts")


@contact_router.post("/", response_model=ContactSchema.Contact)
def create_contact(
    request: Request,
    contact: ContactSchema.ContactCreate = FormDepends(ContactSchema.ContactCreate),
    image: UploadFile | None = None,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [
            UserSchema.UserRoleEnum.ADMIN,
            UserSchema.UserRoleEnum.STAFF,
        ]:
            created_contact = ContactService.create_contact(
                db, contact, image, current_user
            )
            return created_with_location(request, str(created_contact.id))
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@contact_router.get("/", response_model=Page[ContactSchema.Contact])
def read_contacts(
    contact_filter: ContactModel.ContactFilter = FilterDepends(
        ContactModel.ContactFilter
    ),
    page: int = 1,
    size: int = 20,
    sort: str = "created_on",
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [
            UserSchema.UserRoleEnum.ADMIN,
            UserSchema.UserRoleEnum.STAFF,
        ]:
            contacts = ContactRepository.get_contacts(
                db, page=page, size=size, sort=sort, contact_filter=contact_filter
            )
            return contacts
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@contact_router.get("/{contact_id}", response_model=ContactSchema.Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [
            UserSchema.UserRoleEnum.ADMIN,
            UserSchema.UserRoleEnum.STAFF,
        ]:
            return ContactService.get_contact(db, contact_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@contact_router.put("/{contact_id}")
def update_contact(
    contact_id: int,
    contact: ContactSchema.ContactUpdate = FormDepends(ContactSchema.ContactUpdate),
    image: UploadFile | None = None,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [
            UserSchema.UserRoleEnum.ADMIN,
            UserSchema.UserRoleEnum.STAFF,
        ]:
            ContactService.update_contact(db, contact_id, contact, image, current_user)
            return Response(None, status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@contact_router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [
            UserSchema.UserRoleEnum.ADMIN,
            UserSchema.UserRoleEnum.STAFF,
        ]:
            ContactService.delete_contact(db, contact_id)
            return Response(None, status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
