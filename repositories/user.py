from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from configs.Database import get_db_connection
from models.user import User
from repositories.mixins.crud import CRUDRepositoryMixin


class UserRepository(CRUDRepositoryMixin):
    def __init__(self, db: AsyncSession = Depends(get_db_connection)):
        super().__init__(User, db)
