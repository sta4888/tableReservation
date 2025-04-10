from pydantic import BaseModel

class TableCreate(BaseModel):
    name: str
    seats: int
    location: str

class TableResponse(TableCreate):
    id: int

    class Config:
        from_attributes = True