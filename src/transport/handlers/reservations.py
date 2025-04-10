from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from models import Reservation
from repositories.reservation_repository import ReservationRepository
from repositories.table_repository import TableRepository
from schemas.schemas import ReservationCreate, ReservationRead

tag_reservations = {
    "name": "Reservations",
    "description": "Управление бронями столиков",
}

router = APIRouter()


def get_reservation_repository(session: AsyncSession = Depends(get_session)):
    return ReservationRepository(session)


def get_table_repository(session: AsyncSession = Depends(get_session)):
    return TableRepository(session)


@router.get("/", response_model=list[ReservationRead])
async def get_reservations(
    repository: ReservationRepository = Depends(get_reservation_repository),
):
    return await repository.get_all()


@router.post("/", response_model=ReservationRead)
async def create_reservation(
    reservation: ReservationCreate,
    repository: ReservationRepository = Depends(get_reservation_repository),
):
    try:
        return await repository.create(Reservation(**reservation.dict()))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{reservation_id}", status_code=204)
async def delete_reservation(
    reservation_id: int,
    repository: ReservationRepository = Depends(get_reservation_repository),
):
    try:
        await repository.delete(reservation_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
