from fastapi import FastAPI
from .api.routes.tables import router as tables_router
from .api.routes.reservations import router as reservations_router

app = FastAPI(title="Restaurant Reservation System")

app.include_router(tables_router, prefix="/tables", tags=["tables"])
app.include_router(reservations_router, prefix="/reservations", tags=["reservations"])