from datetime import datetime

import pytest

from models.models import Table


@pytest.mark.asyncio
async def test_create_table(client, session):
    response = await client.post(
        "/api/v1/tables/",
        json={"name": "New Table", "seats": 4, "location": "Main Hall"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Table"


@pytest.mark.asyncio
async def test_get_tables(client, session):
    table = Table(name="Test Table", seats=4, location="Main Hall")
    session.add(table)
    await session.commit()

    response = await client.get("/api/v1/tables/")
    assert response.status_code == 200
    tables = response.json()
    assert len(tables) > 0


@pytest.mark.asyncio
async def test_delete_table(client, session):
    table = Table(name="Test Table", seats=4, location="Main Hall")
    session.add(table)
    await session.commit()
    await session.refresh(table)

    response = await client.delete(f"/api/v1/tables/{table.id}")
    assert response.status_code == 204


@pytest.mark.asyncio
@pytest.mark.skip
async def test_delete_nonexistent_table(client):
    response = await client.delete("/api/v1/tables/99999")
    assert response.status_code == 404
