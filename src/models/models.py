from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer
from sqlmodel import Field, Relationship, SQLModel

from models.mixins import TimeStampMixin


class Table(SQLModel, TimeStampMixin, table=True):
    """
    Модель для описания столика в ресторане.
    """

    id: Optional[int] = Field(default=None, primary_key=True, title="Идентификатор")
    name: str = Field(title="Название столика", min_length=1, max_length=100)
    seats: int = Field(
        title="Количество мест",
        ge=1,  # Добавляем ограничение на уровне SQLModel
        sa_column=Column(Integer, nullable=False),
    )
    location: str = Field(title="Расположение", min_length=2, max_length=255)

    reservations: list["Reservation"] = Relationship(back_populates="table")


class Reservation(SQLModel, TimeStampMixin, table=True):
    """
    Модель для бронирования столика.
    """

    id: Optional[int] = Field(default=None, primary_key=True, title="Идентификатор")
    customer_name: str = Field(title="Имя клиента", min_length=1, max_length=100)
    table_id: int = Field(foreign_key="table.id", title="ID столика")
    reservation_time: datetime = Field(
        title="Время бронирования",
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    duration_minutes: int = Field(title="Длительность в минутах")

    table: Optional[Table] = Relationship(back_populates="reservations")
