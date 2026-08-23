import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier

from app.ml.train_model import XGBoostClassifier, select_best_algorithm


def _perfectly_separable_data() -> tuple[pd.DataFrame, pd.Series]:
    # "signal" == 1 luôn là "late", "signal" == 0 luôn là "on_time" — thuật toán học được
    # quy tắc này phải đạt recall hoàn hảo, thuật toán không học gì (luôn đoán on_time) phải
    # đạt recall 0 trên lớp "late".
    on_time_rows = [{"signal": 0} for _ in range(25)]
    late_rows = [{"signal": 1} for _ in range(10)]
    X = pd.DataFrame(on_time_rows + late_rows)
    y = pd.Series(["on_time"] * 25 + ["late"] * 10)
    return X, y


def test_select_best_algorithm_picks_the_candidate_with_highest_late_recall() -> None:
    X, y = _perfectly_separable_data()
    candidates = {
        "always_on_time": DummyClassifier(strategy="constant", constant="on_time"),
        "learns_the_signal": DecisionTreeClassifier(random_state=0),
    }

    winner_name, winner, scores = select_best_algorithm(X, y, candidates, cv_folds=5)

    assert winner_name == "learns_the_signal"
    assert scores["always_on_time"] == 0.0
    assert scores["learns_the_signal"] == 1.0


def test_select_best_algorithm_returns_a_fitted_winner() -> None:
    X, y = _perfectly_separable_data()
    candidates = {
        "always_on_time": DummyClassifier(strategy="constant", constant="on_time"),
        "learns_the_signal": DecisionTreeClassifier(random_state=0),
    }

    _, winner, _ = select_best_algorithm(X, y, candidates, cv_folds=5)

    assert list(winner.predict(X)) == list(y)


def test_xgboost_classifier_works_with_string_labels() -> None:
    # xgboost.XGBClassifier chỉ chấp nhận nhãn dạng số — wrapper này để nó dùng được
    # trực tiếp nhãn "late"/"on_time" như LogisticRegression/RandomForest, không cần
    # encode/decode ở chỗ gọi.
    X, y = _perfectly_separable_data()

    model = XGBoostClassifier()
    model.fit(X, y)

    predictions = model.predict(X)
    assert set(predictions) <= {"late", "on_time"}
    assert list(predictions) == list(y)

    proba = model.predict_proba(X)
    assert list(model.classes_) == ["late", "on_time"]
    # cột "late" phải cao cho các dòng thực sự "late"
    assert proba[-1][0] > 0.5
