import uuid

from sqlalchemy import String, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.dbSessionConfig import Base

from models.job_attempts import JobAttempt

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda:str(uuid.uuid4()),
    )

    task_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )

    result: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="QUEUED",
        nullable=False,
        index=True
)

    max_attempt: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False
    )

    attempts: Mapped[list["JobAttempt"]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan"
    )