from pydantic import BaseModel


class JwtBase(BaseModel):
    token: str


class Jwt(JwtBase):
    pass