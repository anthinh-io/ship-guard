from datetime import UTC, datetime

from app.ml.predict import OrderFeatures, predict

_FEATURES = OrderFeatures(
    seller_state="SP",
    customer_state="RJ",
    payment_type="credit_card",
    category="toys",
    weight_g=500,
    order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
)


class _FakeModel:
    """Model giả trả về xác suất cố định — dùng để test ngưỡng phân loại mà không cần model thật."""

    classes_ = ["late", "on_time"]

    def __init__(self, late_probability: float) -> None:
        self._late_probability = late_probability

    def predict_proba(self, X: object) -> list[list[float]]:
        return [[self._late_probability, 1 - self._late_probability]]


def test_probability_above_50_percent_is_high_risk() -> None:
    result = predict(_FEATURES, model=_FakeModel(late_probability=0.7))

    assert result.risk_label == "high"
    assert result.risk_probability == 0.7


def test_probability_at_or_below_50_percent_is_low_risk() -> None:
    result = predict(_FEATURES, model=_FakeModel(late_probability=0.5))

    assert result.risk_label == "low"
    assert result.risk_probability == 0.5


def test_probability_well_below_threshold_is_low_risk() -> None:
    result = predict(_FEATURES, model=_FakeModel(late_probability=0.1))

    assert result.risk_label == "low"
    assert result.risk_probability == 0.1
