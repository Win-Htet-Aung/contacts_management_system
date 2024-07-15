from sqlalchemy import Date, Column, Integer, String, ForeignKey, DateTime
from fastapi_filter.contrib.sqlalchemy.filter import Filter
from datetime import datetime
from ..base_class import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True)
    middle_name = Column(String, index=True)
    last_name = Column(String, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=True)
    category = Column(String, index=True)
    email = Column(String, unique=True)
    phone = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    occupation = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address_line1 = Column(String, nullable=True)
    address_line2 = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    timezone = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime, default=datetime.now())
    modified_by = Column(Integer, ForeignKey("users.id"))
    modified_on = Column(DateTime, default=datetime.now())

    @staticmethod
    def get_model_name() -> str:
        return "Contact"


class ContactFilter(Filter):
    category__in: list[str] = []
    city__in: list[str] = []
    country__in: list[str] = []
    company_name__in: list[str] = []
    occupation__in: list[str] = []

    class Constants(Filter.Constants):
        model = Contact
