import uuid
from typing import Sequence

from fastapi import Depends
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.Database import get_db_connection
from models.personality_model import PersonalityModel


class PersonalityModelRepository:
    def __init__(self, db: AsyncSession = Depends(get_db_connection)):
        self._db = db

    async def create(self, opts: PersonalityModel) -> PersonalityModel:
        logger.debug("PersonalityModel - Repository - create")
        self._db.add(opts)
        await self._db.commit()
        await self._db.refresh(opts)
        return opts

    async def get_by_card_id(self, card_id: uuid.UUID) -> Sequence[PersonalityModel]:
        logger.debug("PersonalityModel - Repository - get_by_card_id")
        query = select(PersonalityModel).where(PersonalityModel.card == card_id)

        result = await self._db.execute(query)
        return result.scalars().all()

    async def get_by_vacancy_id(
        self, vacancy_id: uuid.UUID
    ) -> Sequence[PersonalityModel]:
        logger.debug("PersonalityModel - Repository - get_by_vacancy_id")
        query = select(PersonalityModel).where(PersonalityModel.vacancy == vacancy_id)

        result = await self._db.execute(query)
        return result.scalars().all()
