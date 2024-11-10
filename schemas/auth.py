from uuid import UUID

from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
    username: str


class RegisterUserOpts(BaseModel):
    username: str
    password: str
    phone: str | None = None
    email: str | None = None


class UserRegisterResponse(BaseModel):
    id: UUID
    username: str
    phone: str | None = None
    email: str | None = None
