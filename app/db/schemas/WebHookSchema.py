from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class ActivityEnum(str, Enum):
    NOTIFICATION = "notification"

    def __str__(self):
        return self.value


class WebHookBase(BaseModel):
    name: str
    callback_url: str


class WebHookCreate(WebHookBase):
    pass


class WebHookUpdate(WebHookBase):
    pass


class WebHook(WebHookBase):
    id: int
    created_by: int
    created_on: datetime
    modified_by: int
    modified_on: datetime

    class Config:
        from_attributes = True
