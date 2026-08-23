# Ngoại lệ pandas/scikit-learn/xgboost trong backend/app/ml/ — xem docs/adr/0003-xgboost-dependency-placement.md.
import logging
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import make_scorer, recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from app.ml.features import CATEGORICAL_FEATURES, NUMERIC_FEATURES, prepare_features
from app.ml.xgboost_classifier import XGBoostClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[3] / "datasets" / "processed"
MODEL_PATH = Path(__file__).resolve().parents[3] / "models" / "risk_model.joblib"

_LATE_RECALL_SCORER = make_scorer(recall_score, pos_label="late", zero_division=0)


def _build_pipeline(estimator: Any) -> Pipeline:
    preprocessor = ColumnTransformer(
        [
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
            ("numeric", "passthrough", NUMERIC_FEATURES),
        ]
    )
    return Pipeline([("preprocess", preprocessor), ("classifier", estimator)])


def default_candidates(y: pd.Series) -> dict[str, Pipeline]:
    late_count = int((y == "late").sum())
    on_time_count = int((y == "on_time").sum())
    scale_pos_weight = on_time_count / late_count if late_count else 1.0
    return {
        "logistic_regression": _build_pipeline(
            LogisticRegression(class_weight="balanced", max_iter=5000)
        ),
        "random_forest": _build_pipeline(
            RandomForestClassifier(class_weight="balanced", random_state=42, n_jobs=-1)
        ),
        "xgboost": _build_pipeline(
            XGBoostClassifier(scale_pos_weight=scale_pos_weight)
        ),
    }


def select_best_algorithm(
    X: pd.DataFrame,
    y: pd.Series,
    candidates: dict[str, Any],
    cv_folds: int = 5,
    random_state: int = 42,
) -> tuple[str, Any, dict[str, float]]:
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
    scores: dict[str, float] = {}
    for name, estimator in candidates.items():
        recalls = cross_val_score(estimator, X, y, cv=cv, scoring=_LATE_RECALL_SCORER)
        scores[name] = float(recalls.mean())
        logger.info("%s: recall trung bình (lớp 'late') = %.4f", name, scores[name])

    winner_name = max(scores, key=lambda name: scores[name])
    winner = candidates[winner_name]
    winner.fit(X, y)
    return winner_name, winner, scores


def train_and_select(
    train_df: pd.DataFrame, cv_folds: int = 5, random_state: int = 42
) -> tuple[str, Any, dict[str, float]]:
    X, y = prepare_features(train_df)
    candidates = default_candidates(y)
    return select_best_algorithm(X, y, candidates, cv_folds, random_state)


def evaluate_recall(model: Any, test_df: pd.DataFrame) -> float:
    X, y = prepare_features(test_df)
    predictions = model.predict(X)
    return float(recall_score(y, predictions, pos_label="late", zero_division=0))


def main() -> None:
    logger.info("Nạp train.csv/test.csv từ %s", DATA_DIR)
    train_df = pd.read_csv(DATA_DIR / "train.csv")
    test_df = pd.read_csv(DATA_DIR / "test.csv")

    winner_name, model, cv_scores = train_and_select(train_df)
    logger.info("Chọn thuật toán %s (điểm CV: %s)", winner_name, cv_scores)

    test_recall = evaluate_recall(model, test_df)
    logger.info(
        "Recall lớp 'late' trên tập test (chạm một lần duy nhất): %.4f", test_recall
    )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    logger.info("Đã lưu model vào %s", MODEL_PATH)


if __name__ == "__main__":
    main()
