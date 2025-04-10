from fastapi import APIRouter, Depends, HTTPException, Response
from datetime import timedelta

from repositories.repository import get_reservation_repository
from repositories.table_repository import IReservationRepository
from schemas.schemas import ReservationRead, ReservationCreate

tag_reservations = {
    "name": "Reservations",
    "description": "Управление бронями столиков"
}

router = APIRouter()

@router.get("/", response_model=list[ReservationRead])
async def get_reservations(
    repository: IReservationRepository = Depends(get_reservation_repository)
):
    return await repository.get_all()

@router.post("/", response_model=ReservationRead)
async def create_reservation(
    reservation: ReservationCreate,
    repository: IReservationRepository = Depends(get_reservation_repository)
):
    # Проверим наличие столика
    table = await repository.get_by_id(reservation.table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Столик не найден")

    # Вычислим конец новой брони
    new_start = reservation.reservation_time
    new_end = new_start + timedelta(minutes=reservation.duration_minutes)

    # Поиск конфликтов
    conflicts = await repository.find_conflicts(
        table_id=reservation.table_id,
        start_time=new_start,
        end_time=new_end
    )
    if conflicts:
        raise HTTPException(
            status_code=409,
            detail="Столик уже забронирован в указанный временной промежуток",
        )

    return await repository.create(reservation)

@router.delete("/{reservation_id}", status_code=204)
async def delete_reservation(
    reservation_id: int,
    repository: IReservationRepository = Depends(get_reservation_repository)
):
    await repository.delete(reservation_id)
    return Response(status_code=204)