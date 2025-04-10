import pytest
from datetime import datetime, timedelta
from models.models import Table, Reservation


@pytest.mark.asyncio
async def test_create_reservation(client, session):

    table = Table(
        name="Test Table",
        seats=4,
        location="Main Hall"
    )
    session.add(table)
    await session.commit()
    await session.refresh(table)

    response = await client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "Test User",
            "table_id": table.id,
            "reservation_time": datetime.now().isoformat(),
            "duration_minutes": 60
        }
    )
    assert response.status_code == 200
    assert response.json()["customer_name"] == "Test User"


@pytest.mark.asyncio
async def test_get_reservations(client, session):
    # Create a sample reservation
    table = Table(
        name="Test Table",
        seats=4,
        location="Main Hall"
    )
    session.add(table)
    await session.commit()
    await session.refresh(table)

    reservation = Reservation(
        customer_name="Test User",
        table_id=table.id,
        reservation_time=datetime.now(),
        duration_minutes=60
    )
    session.add(reservation)
    await session.commit()

    response = await client.get("/api/v1/reservations/")
    assert response.status_code == 200
    reservations = response.json()
    assert len(reservations) > 0


@pytest.mark.asyncio
async def test_delete_reservation(client, session):
    # Create a reservation to delete
    table = Table(
        name="Test Table",
        seats=4,
        location="Main Hall"
    )
    session.add(table)
    await session.commit()
    await session.refresh(table)

    reservation = Reservation(
        customer_name="Test User",
        table_id=table.id,
        reservation_time=datetime.now(),
        duration_minutes=60
    )
    session.add(reservation)
    await session.commit()
    await session.refresh(reservation)

    response = await client.delete(f"/api/v1/reservations/{reservation.id}")
    assert response.status_code == 204


@pytest.mark.asyncio
@pytest.mark.skip
async def test_delete_nonexistent_reservation(client):
    response = await client.delete("/api/v1/reservations/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.skip
async def test_create_overlapping_reservation(client, session):
    # Create initial reservation
    table = Table(
        name="Test Table",
        seats=4,
        location="Main Hall"
    )
    session.add(table)
    await session.commit()
    await session.refresh(table)

    reservation = Reservation(
        customer_name="Test User",
        table_id=table.id,
        reservation_time=datetime.now(),
        duration_minutes=60
    )
    session.add(reservation)
    await session.commit()

    # Try to create overlapping reservation
    start_time = datetime.now()
    response = await client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "Test User 2",
            "table_id": table.id,
            "reservation_time": (start_time + timedelta(minutes=30)).isoformat(),
            "duration_minutes": 30
        }
    )
    assert response.status_code == 409


@pytest.mark.asyncio
@pytest.mark.skip
async def test_create_reservation_with_nonexistent_table(client):
    response = await client.post(
        "/api/v1/reservations/",
        json={
            "customer_name": "Test User",
            "table_id": 99999,
            "reservation_time": datetime.now().isoformat(),
            "duration_minutes": 60
        }
    )
    assert response.status_code == 404