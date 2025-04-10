from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from integrations.db.session import get_session
from repositories.base_repository import ITableRepository, IReservationRepository
from repositories.table_repository import TableRepository, ReservationRepository


def get_table_repository(session: AsyncSession = Depends(get_session)) -> ITableRepository:
    return TableRepository(session)

def get_reservation_repository(session: AsyncSession = Depends(get_session)) -> IReservationRepository:
    return ReservationRepository(session)