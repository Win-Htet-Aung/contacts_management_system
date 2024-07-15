from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from fastapi_filter.contrib.sqlalchemy.filter import Filter
from ..base_class import Base


class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True)
    object_type = Column(String, index=True)
    object_name = Column(String, index=True)
    activity = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime, default=datetime.now)

    @staticmethod
    def get_model_name() -> str:
        return "History"


class HistoryFilter(Filter):
    object_type__in: list[str] = []
    activity__in: list[str] = []

    class Constants(Filter.Constants):
        model = History
