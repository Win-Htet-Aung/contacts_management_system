import requests
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..db.schemas import UserSchema, WebHookSchema, HistorySchema, ContactSchema
from ..repository import WebHookRepository


class WebHookHandler:
    def __init__(self, db: Session, name: WebHookSchema.NameEnum):
        self.name = name
        self.db = db

    def targets(self) -> list[WebHookSchema.WebHookBase]:
        return [
            WebHookSchema.WebHookBase(**i.__dict__)
            for i in WebHookRepository.get_webhooks_by_name(self.db, self.name)
        ]

    def notification_handler(self, target: WebHookSchema.WebHookBase, **kwargs):
        history: HistorySchema.HistoryCreate = kwargs["history"]
        contact: ContactSchema.ContactCreate = kwargs["contact"]
        payload = {
            "message": f"{contact.category} {history.object_type} {contact.full_name()} {history.activity} successfully!"
        }
        requests.post(url=target.callback_url, data=payload)

    def handle(self, **kwargs):
        handler_mapping = {
            WebHookSchema.NameEnum.NOTIFICATION: self.notification_handler,
        }
        for target in self.targets():
            handler_mapping[target.name](target, **kwargs)


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
