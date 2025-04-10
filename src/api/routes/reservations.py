from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database import get_db
from ...models.reservation import Reservation
from ...models.table import Table
from ...schemas.reservation import ReservationCreate, ReservationResponse

router = APIRouter()


def check_reservation_overlap(db: Session, table_id: int,
                              reservation_time: datetime,
                              duration_minutes: int):
    end_time = reservation_time + timedelta(minutes=duration_minutes)
    overlapping = db.query(Reservation).filter(
        Reservation.table_id == table_id,
        Reservation.reservation_time < end_time,
        Reservation.reservation_time + timedelta(minutes=Reservation.duration_minutes) > reservation_time
    ).first()
    return overlapping is not None


@router.post("/", response_model=ReservationResponse)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # Check if table exists
    table = db.query(Table).filter(Table.id == reservation.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Check for overlapping reservations
    if check_reservation_overlap(db, reservation.table_id,
                                 reservation.reservation_time,
                                 reservation.duration_minutes):
        raise HTTPException(status_code=400,
                            detail="Table is already reserved for this time")

    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


@router.get("/", response_model=list[ReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()


@router.delete("/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(reservation)
    db.commit()
    return {"message": "Reservation deleted successfully"}