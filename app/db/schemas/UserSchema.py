from pydantic import BaseModel
from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = 'admin'
    STAFF = 'staff'


class UserBase(BaseModel):
    email: str
    username: str
    

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    role: UserRoleEnum

    class Config:
        from_attributes = True
