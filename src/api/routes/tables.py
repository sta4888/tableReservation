from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ...models.table import Table
from ...schemas.table import TableCreate, TableResponse

router = APIRouter()

@router.post("/", response_model=TableResponse)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = Table(**table.model_dump())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    return db_table

@router.get("/", response_model=list[TableResponse])
def get_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()

@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(table)
    db.commit()
    return {"message": "Table deleted successfully"}