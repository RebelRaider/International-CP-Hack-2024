from fastapi import APIRouter

from schemas.auth import (
    Token,
)

router = APIRouter(prefix="/api/v1/metric", tags=["metric"])


@router.get(
    "/status",
    summary="получение токена",
    response_model=Token,
)
async def status():
    return "UP"
