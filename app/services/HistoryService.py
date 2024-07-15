from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from ..db.schemas import HistorySchema, HistoryDetailsSchema, UserSchema
from ..repository import HistoryRepository


def create_history(
    db: Session,
    history: HistorySchema.HistoryCreate,
    obj_id: int,
    payload: dict,
    current_user: UserSchema.User,
):
    activity = history.activity
    created_history = HistoryRepository.create_history(db, history, current_user)
