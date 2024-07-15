from sqlalchemy.orm import Session
from datetime import date
from ..db.schemas import HistorySchema, HistoryDetailsSchema, UserSchema
from ..repository import HistoryRepository


def create_history(
    db: Session,
    history: HistorySchema.HistoryCreate,
    old_data: dict,
    payload: dict,
    current_user: UserSchema.User,
):
    history_details_list: list[HistoryDetailsSchema.HistoryDetailsBase] = []
    for k, v in payload.items():
        if old_data[k] != v:
            history_details_list.append(
                HistoryDetailsSchema.HistoryDetailsBase(
                    field_name=k,
                    previous_value=to_string(old_data[k]),
                    latest_value=to_string(v),
                )
            )
    if history_details_list:
        created_history = HistoryRepository.create_history(db, history, current_user)
        for history_details in history_details_list:
            history_details_create = HistoryDetailsSchema.HistoryDetailsCreate(
                **history_details.model_dump(),
                history_id=created_history.id,
            )
            HistoryRepository.create_history_details(db, history_details_create)


def to_string(value: str | date | None) -> str:
    if value is not None:
        return str(value)
