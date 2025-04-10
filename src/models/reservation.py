from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..api.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"))
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    table = relationship("Table", back_populates="reservations")