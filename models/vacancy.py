import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.BaseModel import EntityMeta
from models.personality_model import PersonalityModel


class Vacancy(EntityMeta):
    __tablename__ = "vacancy"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    title: Mapped[str]
    description: Mapped[str]

    salary: Mapped[int]

    personality_models: Mapped[list["PersonalityModel"]] = relationship()
