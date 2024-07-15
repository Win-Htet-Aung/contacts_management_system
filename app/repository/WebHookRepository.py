from datetime import datetime
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params
from sqlalchemy import select, desc, asc
from ..db.models import WebHookModel
from ..db.schemas import WebHookSchema, UserSchema


def get_webhook(db: Session, webhook_id: int):
    return (
        db.query(WebHookModel.WebHook)
        .filter(WebHookModel.WebHook.id == webhook_id)
        .first()
    )


def get_webhooks(
    db: Session,
    page: int,
    size: int,
    sort: str,
    webhook_filter: WebHookModel.WebHookFilter,
):
    sort_func = asc
    if sort.startswith("-"):
        sort = sort[1:]
        sort_func = desc
    pagination_params = Params(page=page, size=size)
    return paginate(
        db,
        webhook_filter.filter(select(WebHookModel.WebHook)).order_by(
            sort_func(WebHookModel.WebHook.__dict__[sort])
        ),
        pagination_params,
    )


def get_webhooks_by_name(db: Session, name: WebHookSchema.NameEnum):
    return (
        db.query(WebHookModel.WebHook).filter(WebHookModel.WebHook.name == name).all()
    )


def create_webhook(
    db: Session, webhook: WebHookSchema.WebHookCreate, current_user: UserSchema.User
):
    db_webhook = WebHookModel.WebHook(**webhook.model_dump())
    db_webhook.created_by = current_user["id"]
    db_webhook.modified_by = current_user["id"]
    db_webhook.modified_on = datetime.now()
    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)
    return db_webhook


def update_webhook(
    db: Session,
    webhook_id: int,
    webhook: dict,
    current_user: UserSchema.User,
):
    webhook["modified_by"] = current_user["id"]
    webhook["modified_on"] = datetime.now()
    db.query(WebHookModel.WebHook).filter(WebHookModel.WebHook.id == webhook_id).update(
        webhook
    )
    db.commit()


def delete_webhook(db: Session, webhook_id: int):
    db.query(WebHookModel.WebHook).filter(
        WebHookModel.WebHook.id == webhook_id
    ).delete()
    db.commit()
