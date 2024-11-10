import uuid
from datetime import datetime

from pydantic import BaseModel


class PersonalityModelSchema(BaseModel):
    id: uuid.UUID
    model: str
    parameter: str
    confidence: float

    created_at: datetime
    updated_at: datetime


class CreatePersonalityModel(BaseModel):
    model: str
    parameter: str
    confidence: float
    card: uuid.UUID | None = None
    vacancy: uuid.UUID | None = None
