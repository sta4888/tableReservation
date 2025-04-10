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
    customer_name: str
    table_id: Optional[int] = None  # Добавляем Optional
    reservation_time: datetime
    duration_minutes: int

class ReservationCreate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True