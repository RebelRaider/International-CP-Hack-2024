from fastapi import APIRouter, Depends

from models.user import User
from schemas.personality_models import PersonalityModelSchema, CreatePersonalityModel
from services.auth import authenticated
from services.personality_model import PersonalityModelService

router = APIRouter(prefix="/api/v1/personality_model", tags=["personality_model"])


@router.post(
    "/", summary="creating personality model", response_model=PersonalityModelSchema
)
async def create(
    opts: CreatePersonalityModel,
    personality_model_service: PersonalityModelService = Depends(),
    _: User = Depends(authenticated),
):
    return await personality_model_service.create(opts)
