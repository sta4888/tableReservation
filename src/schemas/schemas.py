from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from pytz import timezone



class TableBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    seats: int = Field(..., ge=1)
    location: str = Field(..., min_length=2, max_length=255)


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int

    class Config:
        from_attributes = True


class ReservationBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    table_id: int

    @validator('reservation_time', pre=True)
    def parse_reservation_time(cls, v):
        """Преобразуем время в формат с временной зоной"""
        if isinstance(v, str):
            # Преобразуем строку в datetime
            dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
            # Устанавливаем временную зону по умолчанию (например, UTC)
            return dt.astimezone(timezone('UTC'))
        return v

    reservation_time: datetime
    duration_minutes: int = Field(..., gt=0)


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: int

    class Config:
        from_attributes = True