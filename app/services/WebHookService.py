from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..db.schemas import UserSchema, WebHookSchema
from ..repository import WebHookRepository


def create_webhook(
    db: Session,
    current_user: UserSchema.User,
    webhook: WebHookSchema.WebHookCreate,
):
    created_webhook = WebHookRepository.create_webhook(db, webhook, current_user)
    return created_webhook


def get_webhook(db: Session, webhook_id: int):
    db_webhook = WebHookRepository.get_webhook(db, webhook_id)
    if db_webhook is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_webhook


def update_webhook(
    db: Session,
    webhook_id: int,
    webhook: WebHookSchema.WebHookUpdate,
    current_user: UserSchema.User,
):
    WebHookRepository.update_webhook(db, webhook_id, webhook, current_user)


def delete_webhook(db: Session, webhook_id: int):
    WebHookRepository.delete_webhook(db, webhook_id)
