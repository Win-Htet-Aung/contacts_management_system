from sqlalchemy import Column, Integer, ForeignKey, String
from ..base_class import Base


class HistoryDetails(Base):
    __tablename__ = "history_details"

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey("histories.id"))
    field_name = Column(String)
    previous_value = Column(String, nullable=True)
    latest_value = Column(String, nullable=True)

    @staticmethod
    def get_model_name() -> str:
        return "HistoryDetails"
