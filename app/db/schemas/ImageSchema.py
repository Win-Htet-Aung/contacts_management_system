from pydantic import BaseModel
from enum import Enum
from datetime import date, datetime


class ImageBase(BaseModel):
    file_url: str


class ContactCreate(ImageBase):
    pass


class Contact(ImageBase):
    id: int
    created_by: int
    created_on: datetime
    modified_by: int
    modified_on: datetime

    class Config:
        from_attributes = True
