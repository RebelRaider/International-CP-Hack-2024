from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from errors.errors import ErrBadRequest
from models.user import User
from schemas.auth import (
    UserAuth,
    TokenData,
    Token,
    UserRegisterResponse,
    RegisterUserOpts,
)
from services.auth import AuthService, authenticated

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/token",
    summary="получение токена",
    response_model=Token,
)
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    user = await auth_service.authenticate_user(
        UserAuth(
            username=form_data.username,
            password=form_data.password,
        )
    )

    access_token = auth_service.create_token(
        {
            "user": TokenData(
                id=str(user.id),
                username=user.username,
            ).model_dump()
        }
    )

    return Token(access_token=access_token, token_type="Bearer")


@router.post(
    "/register",
    summary="регистрация",
    response_model=UserRegisterResponse,
)
async def register(
    opts: RegisterUserOpts,
    auth_service: AuthService = Depends(),
):
    validate_user(opts)
    user = await auth_service.register_user(opts)

    return UserRegisterResponse(
        id=user.id,
        username=user.username,
        phone=user.phone,
        email=user.email,
    )


@router.post(
    "/me",
    summary="получение пользователя",
    response_model=UserRegisterResponse,
)
async def me(
    user: User = Depends(authenticated),
):
    return user


def validate_user(opts: RegisterUserOpts):
    if opts.username == "":
        raise ErrBadRequest("the username cannot be empty")

    if opts.password == "":
        raise ErrBadRequest("the password cannot be empty")
