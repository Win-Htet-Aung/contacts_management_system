from pydantic import BaseModel
from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"


class UserBase(BaseModel):
    username: str


class UserLogin(UserBase):
    password: str


class UserCreate(UserBase):
    email: str
    password: str


class User(UserBase):
    id: int
    email: str
    is_active: bool
    role: UserRoleEnum

    class Config:
        from_attributes = True
