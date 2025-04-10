from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select

from integrations.db.session import get_session
from models.models import Table
from schemas.schemas import TableRead, TableCreate

tag_tables = {
    "name": "Tables",
    "description": "Управление столиками в ресторане"
}

router = APIRouter()


@router.get("/", response_model=list[TableRead])
async def get_tables(session: Session = Depends(get_session)):
    result = await session.execute(select(Table))
    return result.scalars().all()


@router.post("/", response_model=TableRead)
async def create_table(
    table: TableCreate,
    session: Session = Depends(get_session)
):
    db_table = Table(**table.dict())
    session.add(db_table)
    await session.commit()
    await session.refresh(db_table)
    return db_table


@router.delete("/{table_id}", status_code=204)
async def delete_table(
        table_id: int,
        session: AsyncSession = Depends(get_session),
        response: Response = None  # Добавляем параметр Response
):
    """Удаление столика."""
    table = await session.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Столик не найден")

    await session.delete(table)
    await session.commit()

    # Устанавливаем пустой ответ
    response.status_code = 204
    return Response(status_code=204)

