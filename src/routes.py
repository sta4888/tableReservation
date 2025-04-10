from fastapi import FastAPI

from transport.handlers import reservations, tables
from transport.handlers.reservations import tag_reservations
from transport.handlers.tables import tag_tables

metadata_tags = [tag_tables, tag_reservations]


def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов для API"""

    app.include_router(
        tables.router, prefix="/api/v1/tables", tags=[tag_tables["name"]]
    )
    app.include_router(
        reservations.router,
        prefix="/api/v1/reservations",
        tags=[tag_reservations["name"]],
    )
