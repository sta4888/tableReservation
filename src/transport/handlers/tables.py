from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from repositories.repository import get_table_repository
from repositories.table_repository import ITableRepository
from repositories.table_repository import TableRepository


from schemas.schemas import TableRead, TableCreate

tag_tables = {
    "name": "Tables",
    "description": "Управление столиками в ресторане"
}

router = APIRouter()

@router.get("/", response_model=list[TableRead])
async def get_tables(
    repository: ITableRepository = Depends(get_table_repository)
):
    return await repository.get_all()

@router.post("/", response_model=TableRead)
async def create_table(
    table: TableCreate,
    repository: ITableRepository = Depends(get_table_repository)
):
    return await repository.create(table)

@router.delete("/{table_id}", status_code=204)
async def delete_table(
    table_id: int,
    repository: ITableRepository = Depends(get_table_repository)
):
    await repository.delete(table_id)
    return Response(status_code=204)