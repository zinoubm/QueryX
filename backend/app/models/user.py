from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func

from app.db import Base


if TYPE_CHECKING:
    from app.models.document import Document


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    documents: Mapped["Document"] = relationship(
        back_populates="user", cascade="all, delete"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.email!r})"


# add activated column
