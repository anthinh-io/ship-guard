import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.models import Order

client = TestClient(app)


def _make_order(
    session: Session, *, estimated: datetime, actual: datetime | None
) -> None:
    order = Order(
        order_code=f"test-{uuid.uuid4().hex}",
        estimated_delivery_date=estimated,
        actual_delivery_date=actual,
    )
    session.add(order)
    session.commit()


def test_kpi_with_on_time_and_late_orders(db: Session) -> None:
    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    _make_order(db, estimated=estimated, actual=estimated)  # on_time
    _make_order(db, estimated=estimated, actual=estimated + timedelta(days=2))  # late

    response = client.get("/api/v1/dashboard/kpi")

    assert response.status_code == 200
    data = response.json()
    assert data["on_time_count"] == 1
    assert data["late_count"] == 1
    assert data["on_time_rate"] == 0.5
    assert data["late_rate"] == 0.5


def test_kpi_excludes_undetermined_orders_from_rate(db: Session) -> None:
    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    _make_order(db, estimated=estimated, actual=estimated)  # on_time
    _make_order(db, estimated=estimated, actual=None)  # undetermined

    response = client.get("/api/v1/dashboard/kpi")

    assert response.status_code == 200
    data = response.json()
    assert data["on_time_count"] == 1
    assert data["late_count"] == 0
    assert data["on_time_rate"] == 1.0


def test_kpi_returns_none_rate_when_no_data(db: Session) -> None:
    assert db.exec(select(Order)).first() is None

    response = client.get("/api/v1/dashboard/kpi")

    assert response.status_code == 200
    data = response.json()
    assert data["on_time_count"] == 0
    assert data["late_count"] == 0
    assert data["on_time_rate"] is None
    assert data["late_rate"] is None
