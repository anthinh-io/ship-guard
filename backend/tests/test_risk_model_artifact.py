# Test này chạm dữ liệu/artefact thật (models/risk_model.joblib, datasets/processed/*.csv),
# khác với test_train_model.py/test_predict.py vốn chỉ dùng dữ liệu giả lập nhanh.
from datetime import UTC, datetime

import joblib
import pandas as pd
import pytest
from fastapi.testclient import TestClient

import app.ml.predict as predict_module
from app.main import app
from app.ml.predict import MODEL_PATH, RISK_THRESHOLD, OrderFeatures, predict
from app.ml.train_model import DATA_DIR, evaluate_recall, train_and_select


def test_saved_model_recall_on_real_test_set_exceeds_threshold() -> None:
    model = joblib.load(MODEL_PATH)
    test_df = pd.read_csv(DATA_DIR / "test.csv")

    recall = evaluate_recall(model, test_df)

    assert recall > 0.30


def test_saved_model_predicts_on_real_sample_orders() -> None:
    samples = [
        OrderFeatures(
            seller_state="SP",
            customer_state="RJ",
            payment_type="credit_card",
            category="toys",
            weight_g=500,
            order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
        ),
        OrderFeatures(
            seller_state="PE",
            customer_state="AM",
            payment_type="boleto",
            category="furniture_decor",
            weight_g=12000,
            order_purchase_timestamp=datetime(2024, 6, 15, tzinfo=UTC),
        ),
        OrderFeatures(
            # Giá trị hạng mục chưa từng thấy lúc huấn luyện — kiểm tra
            # OneHotEncoder(handle_unknown="ignore") không làm predict() lỗi.
            seller_state="ZZ",
            customer_state="ZZ",
            payment_type="not_a_real_type",
            category="not_a_real_category",
            weight_g=500,
            order_purchase_timestamp=datetime(2024, 3, 1, tzinfo=UTC),
        ),
    ]

    for features in samples:
        result = predict(features)

        assert result.risk_label in {"high", "low"}
        assert 0.0 <= result.risk_probability <= 1.0
        expected_label = "high" if result.risk_probability > RISK_THRESHOLD else "low"
        assert result.risk_label == expected_label


def test_model_is_loaded_eagerly_at_app_startup() -> None:
    predict_module._model = None  # reset phòng khi test khác đã lazy-load trước đó

    with TestClient(app):
        assert predict_module._model is not None


@pytest.mark.slow
def test_full_training_pipeline_reproduces_passing_recall_on_real_data() -> None:
    train_df = pd.read_csv(DATA_DIR / "train.csv")
    test_df = pd.read_csv(DATA_DIR / "test.csv")

    _, model, _ = train_and_select(train_df)
    recall = evaluate_recall(model, test_df)

    assert recall > 0.30
