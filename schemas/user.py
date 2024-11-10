from pydantic import BaseModel


class UserServiceListOpts(BaseModel):
    username: str
    limit: int
    offset: int


class UserServiceCreateOpts(BaseModel):
    username: str
    password: str
    email: str | None = None
    phone: str | None = None
