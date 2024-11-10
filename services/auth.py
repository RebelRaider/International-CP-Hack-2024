from datetime import timedelta, datetime, timezone
from typing import Type

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from loguru import logger
from passlib.context import CryptContext

from configs.Environment import EnvironmentSettings, get_environment_variables
from models.user import User
from schemas.auth import UserAuth, TokenData, RegisterUserOpts
from schemas.user import UserServiceListOpts, UserServiceCreateOpts
from services.user import UserService
from errors.errors import ErrNotAuthorized


class AuthService:
    def __init__(
        self,
        config: EnvironmentSettings = Depends(get_environment_variables),
        user_service: UserService = Depends(UserService),
    ):
        self.user_service = user_service
        self.config = config
        self._access_token_expire = 60
        self.algorithm = "HS256"
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def authenticate_user(self, opts: UserAuth) -> User:
        logger.debug("Auth - Service - authenticate_user")
        users = await self.user_service.list(
            UserServiceListOpts(username=opts.username, limit=1, offset=0)
        )

        if len(users) == 0:
            raise ErrNotAuthorized("the email or password is incorrect")

        user = users[0]

        if not self.verify_password(opts.password, user.password):
            raise ErrNotAuthorized("the email or password is incorrect")

        return user

    async def register_user(self, opts: RegisterUserOpts) -> User:
        logger.debug("Auth - Service - register_user")

        hashed_password = self.get_password_hash(opts.password)

        user = await self.user_service.create(
            UserServiceCreateOpts(
                username=opts.username,
                password=hashed_password,
                phone=opts.phone,
                email=opts.email,
            )
        )

        return user

    def create_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=1)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.config.SECRET_KEY, algorithm=self.algorithm
        )
        return encoded_jwt

    def get_password_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)


async def authenticated(
    token: OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token") = Depends(),
    auth_service: AuthService = Depends(),
) -> Type[User]:
    logger.debug("Auth - Service - get_current_user")

    try:
        payload = jwt.decode(
            token, auth_service.config.SECRET_KEY, algorithms=[auth_service.algorithm]
        )
    except JWTError:
        raise ErrNotAuthorized("cannot decode token")

    token_data: TokenData = payload.get("user")
    if token_data is None:
        raise ErrNotAuthorized("there is no payload in token")

    user = await auth_service.user_service.get(token_data["id"])
    if user is None:
        raise ErrNotAuthorized("there is no user with such id")

    return user
