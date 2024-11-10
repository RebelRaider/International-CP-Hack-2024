import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.BaseModel import EntityMeta
from models.personality_model import PersonalityModel


class Card(EntityMeta):
    __tablename__ = "card"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    video_path: Mapped[str] = mapped_column(nullable=True)
    transcription: Mapped[str] = mapped_column(nullable=True)

    resume_path: Mapped[str] = mapped_column(nullable=True)  # pdf

    motivation_letter: Mapped[str] = mapped_column(nullable=True)

    personality_models: Mapped[list["PersonalityModel"]] = relationship()

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now, nullable=False
    )
