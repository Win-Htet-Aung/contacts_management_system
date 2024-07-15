from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, select
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from ..db.models import HistoryModel, HistoryDetailsModel
from ..db.schemas import HistorySchema, UserSchema, HistoryDetailsSchema


def get_histories(
    db: Session,
    page: int,
    size: int,
    sort: str,
    history_filter: HistoryModel.HistoryFilter,
):
    sort_func = asc
    if sort.startswith("-"):
        sort = sort[1:]
        sort_func = desc
    pagination_params = Params(page=page, size=size)
    return paginate(
        db,
        history_filter.filter(select(HistoryModel.History)).order_by(
            sort_func(HistoryModel.History.__dict__[sort])
        ),
        pagination_params,
    )


def get_history_details(
    db: Session,
    history_id: int,
    page: int,
    size: int,
    sort: str,
    history_details_filter: HistoryDetailsModel.HistoryDetailsFilter,
):
    sort_func = asc
    if sort.startswith("-"):
        sort = sort[1:]
        sort_func = desc
    pagination_params = Params(page=page, size=size)
    return paginate(
        db,
        history_details_filter.filter(
            select(HistoryDetailsModel.HistoryDetails).filter(
                HistoryDetailsModel.HistoryDetails.history_id == history_id
            )
        ).order_by(sort_func(HistoryDetailsModel.HistoryDetails.__dict__[sort])),
        pagination_params,
    )


def get_history(db: Session, history_id: int):
    return (
        db.query(HistoryModel.History)
        .filter(HistoryModel.History.id == history_id)
        .first()
    )


def create_history(
    db: Session, history: HistorySchema.HistoryCreate, current_user: UserSchema.User
):
    db_history = HistoryModel.History(**history.model_dump())
    db_history.created_by = current_user["id"]
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history


def create_history_details(
    db: Session, history_details: HistoryDetailsSchema.HistoryDetailsCreate
):
    db_history_details = HistoryDetailsModel.HistoryDetails(
        **history_details.model_dump()
    )
    db.add(db_history_details)
    db.commit()
    db.refresh(db_history_details)
    return db_history_details
