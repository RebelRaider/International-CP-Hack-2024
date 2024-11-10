from typing import List

from fastapi import APIRouter, Depends

from models.user import User
from schemas.vacancy import VacancySchema, ListVacancyOpts, CreateVacancyOpts
from services.auth import authenticated
from services.vacancy import VacancyService

router = APIRouter(prefix="/api/v1/vacancy", tags=["vacancy"])


@router.get("/", summary="list of the vacancy", response_model=List[VacancySchema])
async def get_list(
    offset: int = 0,
    limit: int = 100,
    vacancy_service: VacancyService = Depends(),
    _: User = Depends(authenticated),
):
    vacancies = await vacancy_service.list(ListVacancyOpts(offset=offset, limit=limit))

    return vacancies


@router.post("/", summary="creating the vacancy", response_model=VacancySchema)
async def create(
    opts: CreateVacancyOpts,
    vacancy_service: VacancyService = Depends(),
    _: User = Depends(authenticated),
):
    vacancy = await vacancy_service.create(opts)

    return vacancy
