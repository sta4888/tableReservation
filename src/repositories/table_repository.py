from pydantic import BaseModel

from repositories.base_repository import  IReservationRepository

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from repositories.repository import ITableRepository
from models.models import Table, Reservation

class TableRepository(ITableRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Table]:
        result = await self.session.execute(select(Table))
        return result.scalars().all()

    async def get_by_id(self, table_id: int) -> Optional[Table]:
        return await self.session.get(Table, table_id)

    async def create(self, table: BaseModel) -> Table:
        db_table = Table(**table.dict())
        self.session.add(db_table)
        await self.session.commit()
        await self.session.refresh(db_table)
        return db_table

    async def delete(self, table_id: int) -> None:
        table = await self.get_by_id(table_id)
        if table:
            await self.session.delete(table)
            await self.session.commit()

class ReservationRepository(IReservationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Reservation]:
        result = await self.session.execute(select(Reservation))
        return result.scalars().all()

    async def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        return await self.session.get(Reservation, reservation_id)

    async def create(self, reservation: BaseModel) -> Reservation:
        new_reservation = Reservation(**reservation.dict())
        self.session.add(new_reservation)
        await self.session.commit()
        await self.session.refresh(new_reservation)
        return new_reservation

    async def delete(self, reservation_id: int) -> None:
        reservation = await self.get_by_id(reservation_id)
        if reservation:
            await self.session.delete(reservation)
            await self.session.commit()

    async def find_conflicts(
        self,
        table_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> List[Reservation]:
        conflict_query = select(Reservation).where(
            and_(
                Reservation.table_id == table_id,
                func.timezone('UTC', Reservation.reservation_time) < end_time,
                func.timezone('UTC', Reservation.reservation_time) +
                func.make_interval(0, 0, 0, 0, 0, Reservation.duration_minutes) >
                func.timezone('UTC', start_time)
            )
        )
        result = await self.session.execute(conflict_query)
        return result.scalars().all()

