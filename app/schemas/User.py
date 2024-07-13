from pydantic import BaseModel
from .Item import Item
from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = 'admin'
    STAFF = 'staff'


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    role: UserRoleEnum
    items: list[Item] = []

    class Config:
        orm_mode = True
