from pydantic import BaseModel
from datetime import datetime



class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

class ReservationResponse(ReservationCreate):
    id: int

    class Config:
        from_attributes = True