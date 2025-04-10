from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from models.models import Reservation, Table
from pydantic import BaseModel

class ITableRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Table]:
        pass

    @abstractmethod
    async def get_by_id(self, table_id: int) -> Optional[Table]:
        pass

    @abstractmethod
    async def create(self, table: BaseModel) -> Table:
        pass

    @abstractmethod
    async def delete(self, table_id: int) -> None:
        pass

class IReservationRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Reservation]:
        pass

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        pass

    @abstractmethod
    async def create(self, reservation: BaseModel) -> Reservation:
        pass

    @abstractmethod
    async def delete(self, reservation_id: int) -> None:
        pass

    @abstractmethod
    async def find_conflicts(
        self,
        table_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> List[Reservation]:
        pass