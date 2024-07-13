from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..base_class import Base
from ..schemas.UserSchema import UserRoleEnum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String)
    hashed_password = Column(String)
    role = Column(String, default=UserRoleEnum.STAFF)
    is_active = Column(Boolean, default=True)
