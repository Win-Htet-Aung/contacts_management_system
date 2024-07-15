from pydantic import BaseModel


class HistoryDetailsBase(BaseModel):
    field_name: str
    previous_value: str | None
    latest_value: str | None


class HistoryDetailsCreate(HistoryDetailsBase):
    history_id: int


class HistoryDetails(HistoryDetailsCreate):
    id: int

    class Config:
        from_attributes = True
