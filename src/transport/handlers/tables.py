from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from integrations.db.session import get_session
from models import Table
from repositories.table_repository import TableRepository
from schemas.schemas import TableRead, TableCreate

tag_tables = {
    "name": "Tables",
    "description": "Управление столиками в ресторане"
}

router = APIRouter()


def get_table_repository(session: AsyncSession = Depends(get_session)):
    return TableRepository(session)


@router.get("/", response_model=list[TableRead])
async def get_tables(
        repository: TableRepository = Depends(get_table_repository)
):
    return await repository.get_all()


@router.post("/", response_model=TableRead)
async def create_table(
        table: TableCreate,
        repository: TableRepository = Depends(get_table_repository)
):
    return await repository.create(Table(**table.dict()))


@router.delete("/{table_id}", status_code=204)
async def delete_table(
        table_id: int,
        repository: TableRepository = Depends(get_table_repository)
):
    try:
        await repository.delete(table_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
