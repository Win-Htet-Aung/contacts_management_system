from pydantic import BaseModel
from enum import Enum
from datetime import date, datetime


class ContactCategoryEnum(str, Enum):
    ALLCONTACTS = "All Contacts"
    CUSTOMER = "Customers"
    PARTNER = "Partners"
    EMPLOYEE = "Employees"


class ContactBase(BaseModel):
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    image_id: int
    category: str
    email: str
    phone: str
    company_name: str
    birth_date: date
    occupation: str
    gender: str
    country: str
    city: str
    address_line1: str
    address_line2: str
    state: str
    zip_code: str
    timezone: str


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    created_by: int
    created_on: datetime
    modified_by: int
    modified_on: datetime

    class Config:
        from_attributes = True
