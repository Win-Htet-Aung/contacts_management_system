from sqlalchemy import Date, Column, Integer, String, ForeignKey, DateTime

from ..base_class import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, index=True)
    middle_name = Column(String, index=True)
    last_name = Column(String, index=True)
    image_id = Column(Integer, ForeignKey("images.id"))
    category = Column(String, index=True)
    email = Column(String)
    phone = Column(String)
    company_name = Column(String)
    birth_date = Column(Date)
    occupation = Column(String)
    gender = Column(String)
    country = Column(String)
    city = Column(String)
    address_line1 = Column(String)
    address_line2 = Column(String)
    state = Column(String)
    zip_code = Column(String)
    timezone = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime)
    modified_by = Column(Integer, ForeignKey("users.id"))
    modified_on = Column(DateTime)
