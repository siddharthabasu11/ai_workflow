from datetime import datetime

from sqlalchemy import DateTime,Integer,String,func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index = True
    )

    github_url : Mapped[str] = mapped_column(
        String(500),
        unique = True,
        nullable = False
    )
    owner : Mapped[str] = mapped_column(
        String(100),
        nullable = False
    )
    name : Mapped[str] = mapped_column(
        String(100),
        nullable = False
    )
    status : Mapped[str] = mapped_column(
        String(30),
        default = "pending",
        nullable = False
    )
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
