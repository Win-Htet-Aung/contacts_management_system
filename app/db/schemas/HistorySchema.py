from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class ActivityEnum(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class HistoryBase(BaseModel):
    object_type: str
    object_name: str
    activity: ActivityEnum


class HistoryCreate(HistoryBase):
    pass


class History(HistoryBase):
    id: int
    created_by: int
    created_on: datetime

    class Config:
        from_attributes = True
