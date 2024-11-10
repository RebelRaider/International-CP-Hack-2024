from typing import Sequence

from fastapi import Depends
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from configs.Database import get_db_connection
from models.vacancy import Vacancy
from schemas.vacancy import ListVacancyOpts


class VacancyRepository:
    def __init__(self, db: AsyncSession = Depends(get_db_connection)):
        self._db = db

    async def create(self, opts: Vacancy) -> Vacancy:
        logger.debug("Vacancy - Repository - create")

        self._db.add(opts)
        await self._db.commit()
        await self._db.refresh(opts)
        return opts

    async def list(self, opts: ListVacancyOpts) -> Sequence[Vacancy]:
        query = select(Vacancy).limit(opts.limit).offset(opts.offset)

        result = await self._db.execute(query)

        return result.scalars().all()
