from pydantic import BaseModel


class HistoryDetailsBase(BaseModel):
    previous_value: str | None
    latest_value: str | None


class HistoryDetailsCreate(HistoryDetailsBase):
    pass


class HistoryDetails(HistoryDetailsBase):
    id: int
    history_id: int

    class Config:
        from_attributes = True
