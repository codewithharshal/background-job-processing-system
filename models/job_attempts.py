import uuid

from sqlalchemy import String,Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.dbSessionConfig import Base

class JobAttempt(Base):
    __tablename__ = "job_attempts"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda:str(uuid.uuid4())
    )

    job_id: Mapped[str]= mapped_column(
        ForeignKey("jobs.id"),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="QUEUED",
        nullable=False,
        index=True
    )

    attempt:Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    job: Mapped["Job"] = relationship(
        back_populates="attempts"
    )