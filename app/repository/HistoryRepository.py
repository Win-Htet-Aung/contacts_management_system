from sqlalchemy.orm import Session
from ..db.models import HistoryModel, HistoryDetailsModel
from ..db.schemas import HistorySchema, UserSchema, HistoryDetailsSchema


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
