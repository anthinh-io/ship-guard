import uuid
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError
from sqlmodel import Session

from app.crud import create_order_with_prediction
from app.models import Order, OrderCreate


class _FakeModel:
    """Model giả trả về xác suất cố định — dùng để test mà không cần model thật."""

    classes_ = ["late", "on_time"]

    def __init__(self, late_probability: float) -> None:
        self._late_probability = late_probability

    def predict_proba(self, X: object) -> list[list[float]]:
        return [[self._late_probability, 1 - self._late_probability]]


def _valid_payload() -> dict:
    return {
        "weight_g": 1500,
        "category": "beleza_saude",
        "payment_type": "credit_card",
        "seller_state": "SP",
        "customer_state": "RJ",
        "order_purchase_timestamp": datetime.now(UTC),
        "estimated_delivery_date": datetime.now(UTC) + timedelta(days=7),
    }


def test_creates_order_with_prediction_attached(db: Session) -> None:
    order_create = OrderCreate(**_valid_payload())

    order = create_order_with_prediction(
        session=db, order_create=order_create, model=_FakeModel(late_probability=0.8)
    )

    assert order.id is not None
    assert uuid.UUID(order.order_code)
    assert order.weight_g == 1500
    assert order.category == "beleza_saude"
    assert order.payment_type == "credit_card"
    assert order.seller_state == "SP"
    assert order.customer_state == "RJ"
    assert order.processing_status == "Chưa xử lý"
    assert order.risk_label == "high"
    assert order.risk_probability == 0.8
    assert order.predicted_at is not None

    fetched = db.get(Order, order.id)
    assert fetched is not None
    assert fetched.risk_label == "high"


def test_rejects_payload_missing_required_field() -> None:
    payload = _valid_payload()
    del payload["payment_type"]

    with pytest.raises(ValidationError):
        OrderCreate(**payload)


def test_rejects_payment_type_outside_fixed_enum() -> None:
    payload = _valid_payload()
    payload["payment_type"] = "not_defined"

    with pytest.raises(ValidationError):
        OrderCreate(**payload)


def test_rejects_state_outside_fixed_enum() -> None:
    payload = _valid_payload()
    payload["seller_state"] = "ZZ"

    with pytest.raises(ValidationError):
        OrderCreate(**payload)
