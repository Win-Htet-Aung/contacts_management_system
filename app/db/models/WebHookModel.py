from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, UniqueConstraint
from datetime import datetime
from fastapi_filter.contrib.sqlalchemy.filter import Filter
from ..base_class import Base


class WebHook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    callback_url = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_on = Column(DateTime, default=datetime.now)
    modified_by = Column(Integer, ForeignKey("users.id"))
    modified_on = Column(DateTime)
    __table_args__ = (
        UniqueConstraint("name", "callback_url", name="_name_callback_url_uc"),
    )

    @staticmethod
    def get_model_name() -> str:
        return "WebHook"


class WebHookFilter(Filter):
    name__in: list[str] = []

    class Constants(Filter.Constants):
        model = WebHook
