import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import Request, Response
from .db.schemas import UserSchema
from .config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def sign_jwt(user: UserSchema.User) -> str:
    payload = {
        "user": user.model_dump(),
        "exp": datetime.now()
        + timedelta(minutes=settings.jwt_access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret_key, settings.jwt_algorithm)


def decode_jwt(token: str) -> UserSchema.User | None:
    try:
        decoded_token = jwt.decode(
            token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm
        )
        if decoded_token["exp"] >= datetime.now().timestamp():
            return decoded_token["user"]
        else:
            return None
    except:
        return None


def created_with_location(request: Request, obj_id: str) -> Response:
    location = f"{request.url}"
    if location.endswith("/"):
        location += obj_id
    else:
        location += f"/{obj_id}"
    return Response(None, status_code=201, headers={"Location": location})
