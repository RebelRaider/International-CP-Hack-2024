import uuid
from typing import List

from pydantic import BaseModel

from schemas.personality_models import PersonalityModelSchema


class VacancySchema(BaseModel):
    id: uuid.UUID
    title: str
    description: str

    salary: int

    personality_models: List[PersonalityModelSchema]


class ListVacancyOpts(BaseModel):
    offset: int = 0
    limit: int = 100


class CreateVacancyOpts(BaseModel):
    title: str
    description: str

    salary: int
