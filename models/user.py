import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from models.BaseModel import EntityMeta


class User(EntityMeta):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(nullable=True, unique=True)

    is_admin: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now, nullable=False
    )
