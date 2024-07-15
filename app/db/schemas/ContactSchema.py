from pydantic import BaseModel
from enum import Enum
from datetime import date, datetime


class ContactCategoryEnum(str, Enum):
    ALLCONTACTS = "All Contacts"
    CUSTOMER = "Customers"
    PARTNER = "Partners"
    EMPLOYEE = "Employees"


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NOTTOSPECIFIED = "not to specified"


class ContactBase(BaseModel):
    middle_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    company_name: str | None = None
    birth_date: date | None = None
    occupation: str | None = None
    country: str | None = None
    city: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    state: str | None = None
    zip_code: str | None = None
    timezone: str | None = None


class ContactCreate(ContactBase):
    first_name: str
    category: ContactCategoryEnum
    gender: GenderEnum
    email: str


class ContactUpdate(ContactBase):
    first_name: str | None = None
    category: ContactCategoryEnum | None = None
    gender: GenderEnum | None = None
    email: str | None = None


class Contact(ContactCreate):
    id: int
    image_id: int | None = None
    created_by: int
    created_on: datetime
    modified_by: int
    modified_on: datetime

    class Config:
        from_attributes = True
