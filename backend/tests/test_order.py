import uuid
from datetime import UTC, datetime, timedelta

from sqlmodel import Session

from app.models import Order


def test_create_and_read_order_round_trip(db: Session) -> None:
    order_code = f"test-{uuid.uuid4().hex}"
    estimated = datetime.now(UTC) + timedelta(days=5)
    order = Order(order_code=order_code, estimated_delivery_date=estimated)

    db.add(order)
    db.commit()
    db.refresh(order)

    fetched = db.get(Order, order.id)
    assert fetched is not None
    assert fetched.order_code == order_code
    assert fetched.estimated_delivery_date == estimated
    assert fetched.actual_delivery_date is None


def test_order_default_processing_status_is_chua_xu_ly(db: Session) -> None:
    order = Order(
        order_code=f"test-{uuid.uuid4().hex}",
        estimated_delivery_date=datetime.now(UTC),
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    assert order.processing_status == "Chưa xử lý"
