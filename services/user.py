from typing import Type, List

from fastapi import Depends

from models.user import User
from repositories.user import UserRepository
from schemas.user import UserServiceCreateOpts, UserServiceListOpts
from services.mixins.crud import CRUDServiceMixin


class UserService(CRUDServiceMixin):
    def __init__(self, repo: UserRepository = Depends()):
        super().__init__(repo)

    async def create(self, req: UserServiceCreateOpts) -> Type[User]:
        user = await self._repo.create(
            User(
                username=req.username,
                password=req.password,
                email=req.email,
                phone=req.phone,
            )
        )

        return user

    async def list(self, opts: UserServiceListOpts) -> List[Type[User]]:
        users = await self._repo.list(opts.limit, opts.offset, username=opts.username)

        return users
