from datetime import datetime

from sqlalchemy import DateTime, Integer, String, JSON, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id"),
        nullable=False
    )

    file_count: Mapped[int] = mapped_column(Integer, nullable=False)
    total_loc: Mapped[int] = mapped_column(Integer, nullable=False)
    language_breakdown: Mapped[dict] = mapped_column(JSON, nullable=False)
    largest_files: Mapped[list] = mapped_column(JSON, nullable=False)
    report: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )