from pydantic import BaseModel
from enum import Enum
from datetime import date, datetime


class ContactCategoryEnum(str, Enum):
    ALLCONTACTS = "All Contacts"
    CUSTOMER = "Customers"
    PARTNER = "Partners"
    EMPLOYEE = "Employees"


class ContactBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    image_id: int|None = None
    category: ContactCategoryEnum
    email: str
    phone: str|None = None
    company_name: str|None = None
    birth_date: date|None = None
    occupation: str|None = None
    gender: str|None = None
    country: str|None = None
    city: str|None = None
    address_line1: str|None = None
    address_line2: str|None = None
    state: str|None = None
    zip_code: str|None = None
    timezone: str|None = None


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    created_by: int|None = None
    created_on: datetime
    modified_by: int|None = None
    modified_on: datetime

    class Config:
        from_attributes = True
