import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.BaseModel import EntityMeta


class PersonalityModel(EntityMeta):
    __tablename__ = "personality_model"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    model: Mapped[str]  # the name of the personality test, e.g OCEAN
    parameter: Mapped[str]  # the parameter from model
    confidence: Mapped[float]  # the confidence for this metric

    card: Mapped[uuid] = mapped_column(ForeignKey("card.id"), nullable=True)

    vacancy: Mapped[uuid] = mapped_column(ForeignKey("vacancy.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now, nullable=False
    )
