from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from exceptions import ObjectNotFoundException, ConflictException
from models.models import Reservation, Table


class ReservationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Reservation]:
        result = await self.session.execute(select(Reservation))
        return result.scalars().all()

    async def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        return await self.session.get(Reservation, reservation_id)

    async def create(self, reservation: Reservation) -> Reservation:
        table = await self.session.get(Table, reservation.table_id)
        if not table:
            raise ObjectNotFoundException(detail="Столик не найден")


        conflict_query = select(Reservation).where(
            and_(
                Reservation.table_id == reservation.table_id,
            )
        )

        conflicts = await self.session.execute(conflict_query)
        if conflicts.scalars().all():
            raise ConflictException(
                detail="Столик уже забронирован в указанный временной промежуток"
            )

        self.session.add(reservation)
        await self.session.commit()
        await self.session.refresh(reservation)
        return reservation

    async def delete(self, reservation_id: int) -> None:
        reservation = await self.get_by_id(reservation_id)
        if not reservation:
            raise ValueError("Бронирование не найдено")

        await self.session.delete(reservation)
        await self.session.commit()
