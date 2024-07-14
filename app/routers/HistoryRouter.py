from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
    UploadFile,
    Response,
)
from sqlalchemy.orm import Session
from pyfa_converter_v2 import FormDepends
from fastapi_pagination import Page
from fastapi_filter import FilterDepends
from ..db.schemas import HistorySchema, HistoryDetailsSchema
from ..db.models import HistoryModel, HistoryDetailsModel
from ..repository import HistoryRepository
from ..services import HistoryService
from ..dependencies import get_db, get_current_user

history_router = APIRouter(prefix="/histories")