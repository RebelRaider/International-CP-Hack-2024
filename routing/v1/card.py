import uuid
from typing import List

from fastapi import Depends, APIRouter, UploadFile, File, Form, HTTPException

from schemas.card import CardSchema, ListCardOpts
from services.card import CardService

router = APIRouter(prefix="/api/v1/card", tags=["card"])


@router.get("/", summary="list of the cards", response_model=List[CardSchema])
async def get_list(
    limit: int = 100,
    offset: int = 0,
    card_service: CardService = Depends(),
):
    cards = await card_service.list(ListCardOpts(offset=offset, limit=limit))

    return cards


@router.get("/{id}", summary="getting card by id", response_model=CardSchema)
async def get(
    id: uuid.UUID,
    card_service: CardService = Depends(),
):
    card = await card_service.get(id)

    return card

@router.get("advice/{id}", summary="getting advice by card id")
async def get(
        id: uuid.UUID,
        card_service: CardService = Depends(),
):
    advice = await card_service.create_advice(id)

    return advice

@router.post("/", summary="creating card", response_model=CardSchema)
async def create(
    pdf_file: UploadFile = File(..., description="Upload a PDF file"),
    video_file: UploadFile = File(..., description="Upload an MP4 video file"),
    motivation_letter: str = Form(..., description="Motivation letter as a string"),
    card_service: CardService = Depends(),
):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type for PDF. Expected application/pdf",
        )

    if video_file.content_type != "video/mp4":
        raise HTTPException(
            status_code=400, detail="Invalid file type for video. Expected video/mp4"
        )

    pdf = await pdf_file.read()
    video = await video_file.read()

    card = await card_service.create(pdf, video, motivation_letter)

    return card


# @router.delete("/", summary="deleting card")
# def delete(card_service: CardService, auth_service: AuthService = Depends(), ):
#
#
# @router.patch("/", summary="updating card")
# def update(card_service: CardService, auth_service: AuthService = Depends(), ):
