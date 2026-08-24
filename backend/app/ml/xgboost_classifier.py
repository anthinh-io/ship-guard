# Ngoại lệ pandas/scikit-learn/xgboost trong backend/app/ml/ — xem docs/adr/0003-xgboost-dependency-placement.md.
#
# Tách riêng khỏi train_model.py: class được pickle vào models/risk_model.joblib, và
# pickle ghi lại đường dẫn module lúc định nghĩa class — nếu class nằm trong train_model.py
# và train_model.py được chạy bằng `python -m app.ml.train_model` (tức __name__ == "__main__"
# lúc đó), joblib.load() ở một tiến trình khác (vd. pytest) sẽ không tìm lại được class.
from typing import Any

import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from xgboost import XGBClassifier

_LABEL_TO_INT = {"on_time": 0, "late": 1}
_INT_TO_LABEL = {0: "on_time", 1: "late"}


class XGBoostClassifier(BaseEstimator, ClassifierMixin):  # type: ignore[misc]
    """Bọc XGBClassifier để dùng trực tiếp nhãn chuỗi "late"/"on_time".

    xgboost.XGBClassifier chỉ chấp nhận nhãn dạng số (0/1), khác với
    LogisticRegression/RandomForestClassifier của scikit-learn vốn chấp nhận
    nhãn chuỗi trực tiếp — wrapper này che đi khác biệt đó.
    """

    def __init__(self, scale_pos_weight: float = 1.0, random_state: int = 42) -> None:
        self.scale_pos_weight = scale_pos_weight
        self.random_state = random_state

    def fit(self, X: pd.DataFrame, y: pd.Series) -> XGBoostClassifier:
        y_encoded = pd.Series(y).map(_LABEL_TO_INT)
        self.classes_ = ["late", "on_time"]
        self._model = XGBClassifier(
            scale_pos_weight=self.scale_pos_weight,
            eval_metric="logloss",
            random_state=self.random_state,
        )
        self._model.fit(X, y_encoded)
        return self

    def predict(self, X: pd.DataFrame) -> list[str]:
        return [_INT_TO_LABEL[p] for p in self._model.predict(X)]

    def predict_proba(self, X: pd.DataFrame) -> Any:
        # self._model.classes_ nội bộ là [0, 1] => cột 0 = P(on_time), cột 1 = P(late).
        # Đảo cột để khớp self.classes_ = ["late", "on_time"].
        proba = self._model.predict_proba(X)
        return proba[:, [1, 0]]
