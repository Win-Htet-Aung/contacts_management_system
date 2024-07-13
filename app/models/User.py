from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..settings.database import Base
from ..schemas.User import UserRoleEnum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default=UserRoleEnum.STAFF)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
