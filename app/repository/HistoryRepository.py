from datetime import datetime
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy import select, desc, asc
from ..db.models import HistoryModel
from ..db.schemas import HistorySchema, UserSchema


def create_history(
    db: Session, history: HistorySchema.HistoryCreate, current_user: UserSchema.User
):
    db_history = HistoryModel.History(**history.model_dump())
    db_history.created_by = current_user["id"]
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history
