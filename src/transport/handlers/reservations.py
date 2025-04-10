from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_, Session

from integrations.db.session import get_session
from models.models import Reservation, Table

from schemas.schemas import ReservationRead, ReservationCreate

tag_reservations = {
    "name": "Reservations",
    "description": "Управление бронями столиков"
}

router = APIRouter()


@router.get("/", response_model=list[ReservationRead])
async def get_reservations(session: Session = Depends(get_session)):
    result = await session.execute(select(Reservation))
    return result.scalars().all()


@router.post("/", response_model=ReservationRead)
async def create_reservation(
    reservation: ReservationCreate,
    session: Session = Depends(get_session)
):
    # Проверим наличие столика
    table = await session.get(Table, reservation.table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Столик не найден")

    # Вычислим конец новой брони
    new_start = reservation.reservation_time
    new_end = new_start + timedelta(minutes=reservation.duration_minutes)

    # Поиск конфликтов
    conflict_query = select(Reservation).where(
        and_(
            Reservation.table_id == reservation.table_id,
            func.timezone('UTC', Reservation.reservation_time) < new_end,
            func.timezone('UTC', Reservation.reservation_time) +
            func.make_interval(0, 0, 0, 0, 0, Reservation.duration_minutes) >
            func.timezone('UTC', new_start)
        )
    )

    conflicts = await session.execute(conflict_query)
    if conflicts.scalars().all():
        raise HTTPException(
            status_code=409,
            detail="Столик уже забронирован в указанный временной промежуток",
        )

    # Создаем новую бронь
    new_reservation = Reservation(**reservation.dict())
    session.add(new_reservation)
    await session.commit()
    await session.refresh(new_reservation)
    return new_reservation


@router.delete("/{reservation_id}", status_code=204)
async def delete_reservation(
        reservation_id: int,
        session: AsyncSession = Depends(get_session)
):
    """Удаление бронирования."""
    reservation = await session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Бронь не найдена")

    await session.delete(reservation)
    await session.commit()

    return Response(status_code=204)