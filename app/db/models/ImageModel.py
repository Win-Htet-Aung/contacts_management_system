from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from ..base_class import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    file_url = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime, default=datetime.now())
    modified_by = Column(Integer, ForeignKey("users.id"))
    modified_on = Column(DateTime, default=datetime.now())
