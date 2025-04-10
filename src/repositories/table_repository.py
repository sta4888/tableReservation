from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import ConflictException, ObjectNotFoundException
from models.models import Reservation, Table


class TableRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Table]:
        result = await self.session.execute(select(Table))
        return result.scalars().all()

    async def get_by_id(self, table_id: int) -> Optional[Table]:
        return await self.session.get(Table, table_id)

    async def create(self, table: Table) -> Table:
        self.session.add(table)
        await self.session.commit()
        await self.session.refresh(table)
        return table

    async def delete(self, table_id: int) -> None:
        table = await self.get_by_id(table_id)
        if not table:
            raise ObjectNotFoundException(detail="Столик не найден")

        result = await self.session.execute(
            select(Reservation).where(Reservation.table_id == table_id)
        )
        if result.scalars().first():
            raise ConflictException(
                detail="Невозможно удалить столик с активными бронированиями"
            )

        await self.session.delete(table)
        await self.session.commit()
