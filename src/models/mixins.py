from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import Column, DateTime, Field


class TimeStampMixin(BaseModel):
    """
    Миксин для добавления атрибутов с датой и временем создания и обновления записи.
    """

    created_at: Optional[datetime] = Field(
        title="Дата и время создания записи",
        sa_column=Column(
            DateTime(timezone=True),
            default=func.now(),
            nullable=False,
        ),
    )
    updated_at: Optional[datetime] = Field(
        title="Дата и время обновления записи",
        sa_column=Column(
            DateTime(timezone=True),
            default=func.now(),
            onupdate=func.now(),
        ),
    )
