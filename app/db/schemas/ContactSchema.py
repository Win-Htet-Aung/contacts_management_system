from pydantic import BaseModel
from enum import Enum
from datetime import date, datetime


class ContactCategoryEnum(str, Enum):
    ALLCONTACTS = "All Contacts"
    CUSTOMER = "Customers"
    PARTNER = "Partners"
    EMPLOYEE = "Employees"


class ContactBase(BaseModel):
    image_id: int | None = None
    phone: str | None = None
    company_name: str | None = None
    birth_date: date | None = None
    occupation: str | None = None
    gender: str | None = None
    country: str | None = None
    city: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    state: str | None = None
    zip_code: str | None = None
    timezone: str | None = None


class ContactCreate(ContactBase):
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    category: ContactCategoryEnum
    email: str


class ContactUpdate(ContactBase):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    category: ContactCategoryEnum | None = None
    email: str | None = None


class Contact(ContactCreate):
    id: int
    created_by: int
    created_on: datetime
    modified_by: int
    modified_on: datetime

    class Config:
        from_attributes = True
