from typing import Optional, List
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlmodel import Field, SQLModel, Relationship

from models.mixins import TimeStampMixin

class Table(SQLModel, TimeStampMixin, table=True):
    """
    Модель для описания столика в ресторане.
    """

    id: Optional[int] = Field(default=None, primary_key=True, title="Идентификатор")
    name: str = Field(title="Название столика", min_length=1, max_length=100)
    seats: int = Field(
        title="Количество мест",
        ge=1,
        sa_column=Column(Integer, nullable=False)
    )
    location: str = Field(title="Расположение", min_length=2, max_length=255)

    # Добавляем каскадное удаление через sa_column
    reservations: list["Reservation"] = Relationship(back_populates="table")

class Reservation(SQLModel, TimeStampMixin, table=True):
    """
    Модель для бронирования столика.
    """

    id: Optional[int] = Field(default=None, primary_key=True, title="Идентификатор")
    customer_name: str = Field(title="Имя клиента", min_length=1, max_length=100)
    table_id: int = Field(
        title="ID столика",
        sa_column=Column(Integer, ForeignKey("table.id", ondelete="CASCADE"))
    )
    reservation_time: datetime = Field(
        title="Время бронирования",
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    duration_minutes: int = Field(title="Длительность в минутах")

    table: Optional[Table] = Relationship(back_populates="reservations")