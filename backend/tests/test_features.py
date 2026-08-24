from datetime import UTC, datetime

import pandas as pd

from app.ml.features import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    add_temporal_features,
    prepare_features,
)


def test_add_temporal_features_extracts_day_of_week_and_month() -> None:
    df = pd.DataFrame(
        {
            "order_purchase_timestamp": [
                datetime(2024, 1, 1, tzinfo=UTC),  # thứ Hai
                datetime(2024, 3, 17, tzinfo=UTC),  # Chủ nhật
            ]
        }
    )

    result = add_temporal_features(df)

    assert result["day_of_week"].tolist() == [0, 6]
    assert result["month"].tolist() == [1, 3]


def test_prepare_features_returns_feature_frame_and_label() -> None:
    df = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "seller_state": ["SP"],
            "customer_state": ["RJ"],
            "payment_type": ["credit_card"],
            "order_purchase_timestamp": [datetime(2024, 1, 1, tzinfo=UTC)],
            "weight_g": [500],
            "category": ["toys"],
            "label": ["on_time"],
        }
    )

    X, y = prepare_features(df)

    assert list(X.columns) == CATEGORICAL_FEATURES + NUMERIC_FEATURES
    assert y.tolist() == ["on_time"]
    assert X["day_of_week"].iloc[0] == 0
    assert X["month"].iloc[0] == 1
