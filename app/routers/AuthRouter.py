from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.schemas import JwtSchema
from ..dependencies import get_db
from ..services import AuthService

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=JwtSchema.Jwt)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return AuthService.login(form_data, db)


@auth_router.post("/logout")
def logout(request: Request):
    print(request)
    return Response(status_code=status.http_2)
