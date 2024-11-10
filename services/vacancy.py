from typing import List

from fastapi import Depends
from loguru import logger

from models.vacancy import Vacancy
from repositories.vacancy import VacancyRepository
from schemas.vacancy import CreateVacancyOpts, VacancySchema, ListVacancyOpts
from services.personality_model import PersonalityModelService


class VacancyService:
    def __init__(
        self,
        repo: VacancyRepository = Depends(),
        pm_service: PersonalityModelService = Depends(),
    ):
        self._pm_service = pm_service
        self._repo = repo

    async def create(self, opts: CreateVacancyOpts) -> VacancySchema:
        logger.debug("Service - Vacancy - create")
        vacancy = await self._repo.create(
            Vacancy(title=opts.title, description=opts.description, salary=opts.salary)
        )

        return await self._vacancy_repo_to_schema(vacancy)

    async def list(self, opts: ListVacancyOpts) -> List[VacancySchema]:
        logger.debug("Service - Vacancy - list")
        vacancies = await self._repo.list(opts)

        return [await self._vacancy_repo_to_schema(vacancy) for vacancy in vacancies]

    async def _vacancy_repo_to_schema(self, req: Vacancy) -> VacancySchema:
        return VacancySchema(
            id=req.id,
            title=req.title,
            description=req.description,
            salary=req.salary,
            personality_models=await self._pm_service.get_by_vacancy_id(req.id),
        )
