# Ngoại lệ pandas/scikit-learn/xgboost trong backend/app/ml/ — xem docs/adr/0003-xgboost-dependency-placement.md.
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import joblib
import pandas as pd

from app.ml.features import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    add_temporal_features,
)

MODEL_PATH = Path(__file__).resolve().parents[3] / "models" / "risk_model.joblib"
RISK_THRESHOLD = 0.5

_model: Any | None = None


@dataclass
class OrderFeatures:
    seller_state: str
    customer_state: str
    payment_type: str
    category: str
    weight_g: float
    order_purchase_timestamp: datetime


@dataclass
class PredictionResult:
    risk_label: Literal["high", "low"]
    risk_probability: float


def _load_model() -> Any:
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict(features: OrderFeatures, model: Any | None = None) -> PredictionResult:
    model = model if model is not None else _load_model()

    df = pd.DataFrame(
        [
            {
                "seller_state": features.seller_state,
                "customer_state": features.customer_state,
                "payment_type": features.payment_type,
                "category": features.category,
                "weight_g": features.weight_g,
                "order_purchase_timestamp": features.order_purchase_timestamp,
            }
        ]
    )
    features_df = add_temporal_features(df)
    X = features_df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]

    late_index = list(model.classes_).index("late")
    probability = float(model.predict_proba(X)[0][late_index])
    risk_label: Literal["high", "low"] = (
        "high" if probability > RISK_THRESHOLD else "low"
    )

    return PredictionResult(risk_label=risk_label, risk_probability=probability)
