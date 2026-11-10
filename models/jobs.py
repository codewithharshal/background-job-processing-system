import uuid

from sqlalchemy import String, JSON, Text,Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.configDatabase import Base

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

    status: Mapped[str] = mapped_column(
        String(20),
        default="QUEUED",
        nullable=False,
        index=True
    )

    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )

    result: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    attempt:Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    max_attempts: Mapped[int] = mapped_column(
        Integer,
        default=5
    )