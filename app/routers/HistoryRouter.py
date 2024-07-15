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
from ..db.schemas import HistorySchema, HistoryDetailsSchema, UserSchema
from ..db.models import HistoryModel, HistoryDetailsModel
from ..repository import HistoryRepository
from ..services import HistoryService
from ..dependencies import get_db, get_current_user

history_router = APIRouter(prefix="/histories")


@history_router.get("/", response_model=Page[HistorySchema.History])
def read_histories(
    history_filter: HistoryModel.HistoryFilter = FilterDepends(
        HistoryModel.HistoryFilter
    ),
    page: int = 1,
    size: int = 20,
    sort: str = "created_on",
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            histories = HistoryRepository.get_histories(
                db, page, size, sort, history_filter
            )
            return histories
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@history_router.get("/{history_id}", response_model=HistorySchema.History)
def read_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            db_history = HistoryRepository.get_history(db, history_id)
            if db_history is None:
                raise HTTPException(status_code=404, detail="History not found")
            return db_history
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@history_router.get(
    "/{history_id}/details", response_model=Page[HistoryDetailsSchema.HistoryDetails]
)
def read_history_details(
    history_id: int,
    history_details_filter: HistoryDetailsModel.HistoryDetailsFilter = FilterDepends(
        HistoryDetailsModel.HistoryDetailsFilter
    ),
    page: int = 1,
    size: int = 20,
    sort: str = "field_name",
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            history_details = HistoryRepository.get_history_details(
                db, history_id, page, size, sort, history_details_filter
            )
            return history_details
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
