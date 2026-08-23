import pandas as pd

CATEGORICAL_FEATURES = ["seller_state", "customer_state", "payment_type", "category"]
NUMERIC_FEATURES = ["weight_g", "day_of_week", "month"]


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    timestamps = pd.to_datetime(df["order_purchase_timestamp"])
    df["day_of_week"] = timestamps.dt.dayofweek
    df["month"] = timestamps.dt.month
    return df


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    features_df = add_temporal_features(df)
    X = features_df[CATEGORICAL_FEATURES + NUMERIC_FEATURES]
    y = features_df["label"]
    return X, y
