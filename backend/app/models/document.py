from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

from app.db import Base

if TYPE_CHECKING:
    from app.models.user import User


class Document(Base):
    __tablename__ = "document"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(GUID, ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="documents")
    name: Mapped[str]

    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
