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
from sqlalchemy.exc import IntegrityError
from pyfa_converter_v2 import FormDepends
from fastapi_pagination import Page
from fastapi_filter import FilterDepends
from psycopg2.errors import UniqueViolation
from ..db.schemas import ContactSchema, UserSchema, WebHookSchema
from ..db.models import ContactModel, WebHookModel
from ..repository import ContactRepository, WebHookRepository
from ..services import ContactService, WebHookService
from ..dependencies import get_db, get_current_user
from ..utils import created_with_location

webhook_router = APIRouter(prefix="/webhooks")


@webhook_router.post("/", response_model=WebHookSchema.WebHook)
def create_webhook(
    request: Request,
    webhook: WebHookSchema.WebHookCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            try:
                created_webhook = WebHookService.create_webhook(
                    db, current_user, webhook
                )
            except IntegrityError as e:
                detail = e._message().split("\n")[-2]
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
            return created_with_location(request, str(created_webhook.id))
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@webhook_router.get("/", response_model=Page[WebHookSchema.WebHook])
def read_webhooks(
    webhook_filter: WebHookModel.WebHookFilter = FilterDepends(
        WebHookModel.WebHookFilter
    ),
    page: int = 1,
    size: int = 20,
    sort: str = "name",
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            webhooks = WebHookRepository.get_webhooks(
                db, page, size, sort, webhook_filter
            )
            return webhooks
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@webhook_router.get("/{webhook_id}", response_model=WebHookSchema.WebHook)
def read_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            return WebHookService.get_webhook(db, webhook_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@webhook_router.put("/{webhook_id}")
def update_webhook(
    webhook_id: int,
    webhook: WebHookSchema.WebHookUpdate,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            WebHookService.update_webhook(db, webhook_id, webhook, current_user)
            return Response(None, status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@webhook_router.delete("/{webhook_id}")
def delete_webhook(
    webhook_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.User | None = Depends(get_current_user),
):
    if current_user:
        if current_user["role"] in [UserSchema.UserRoleEnum.ADMIN]:
            WebHookService.delete_webhook(db, webhook_id)
            return Response(None, status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
