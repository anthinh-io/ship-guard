import uuid
from datetime import UTC, datetime

import pandas as pd
from sqlmodel import Session

from app.ml.prepare_training_data import (
    build_dataset,
    data_quality_report,
    split_train_test,
)
from app.models import Customer, Order, OrderItem, OrderPayment, Product, Seller


def _make_order(
    session: Session,
    *,
    order_code: str | None = None,
    customer_id: str | None = None,
    estimated: datetime,
    actual: datetime | None,
    order_purchase_timestamp: datetime | None,
) -> str:
    order_code = order_code or f"test-{uuid.uuid4().hex}"
    order = Order(
        order_code=order_code,
        customer_id=customer_id,
        estimated_delivery_date=estimated,
        actual_delivery_date=actual,
        order_purchase_timestamp=order_purchase_timestamp,
    )
    session.add(order)
    session.commit()
    return order_code


def _make_complete_order(
    session: Session,
    *,
    order_code: str,
    on_time: bool,
    seller_state: str = "SP",
    customer_state: str = "RJ",
    payment_type: str = "credit_card",
) -> None:
    customer_id = f"cust-{order_code}"
    seller_id = f"seller-{order_code}"
    product_id = f"prod-{order_code}"
    session.add(Customer(customer_id=customer_id, customer_state=customer_state))
    session.add(Seller(seller_id=seller_id, seller_state=seller_state))
    session.commit()

    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    actual = (
        datetime(2024, 1, 10, tzinfo=UTC)
        if on_time
        else datetime(2024, 1, 15, tzinfo=UTC)
    )
    _make_order(
        session,
        order_code=order_code,
        customer_id=customer_id,
        estimated=estimated,
        actual=actual,
        order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
    )
    session.add(
        Product(product_id=product_id, weight_g=500, category_name_english="toys")
    )
    session.add(
        OrderItem(
            order_id=order_code,
            order_item_id=1,
            product_id=product_id,
            seller_id=seller_id,
        )
    )
    session.add(
        OrderPayment(
            order_id=order_code,
            payment_sequential=1,
            payment_type=payment_type,
            payment_installments=1,
            payment_value=100.0,
        )
    )
    session.commit()


def test_delivered_orders_labeled_on_time_and_late(db: Session) -> None:
    _make_complete_order(db, order_code="order-on-time", on_time=True)
    _make_complete_order(db, order_code="order-late", on_time=False)

    df = build_dataset(db)

    labels = dict(zip(df["order_id"], df["label"], strict=True))
    assert labels["order-on-time"] == "on_time"
    assert labels["order-late"] == "late"


def test_undetermined_order_excluded(db: Session) -> None:
    _make_order(
        db,
        estimated=datetime(2024, 1, 10, tzinfo=UTC),
        actual=None,
        order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
    )

    df = build_dataset(db)

    assert len(df) == 0


def test_order_missing_payment_excluded(db: Session) -> None:
    customer_id = "cust-1"
    seller_id = "seller-1"
    db.add(Customer(customer_id=customer_id, customer_state="RJ"))
    db.add(Seller(seller_id=seller_id, seller_state="SP"))
    db.commit()

    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(
        db,
        customer_id=customer_id,
        estimated=estimated,
        actual=estimated,
        order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
    )
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=1,
            product_id="prod-1",
            seller_id=seller_id,
        )
    )
    db.commit()
    # Cố ý không thêm OrderPayment nào cho đơn này.

    df = build_dataset(db)

    assert len(df) == 0


def test_order_missing_purchase_timestamp_excluded(db: Session) -> None:
    customer_id = "cust-1"
    seller_id = "seller-1"
    db.add(Customer(customer_id=customer_id, customer_state="RJ"))
    db.add(Seller(seller_id=seller_id, seller_state="SP"))
    db.commit()

    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(
        db,
        customer_id=customer_id,
        estimated=estimated,
        actual=estimated,
        order_purchase_timestamp=None,
    )
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=1,
            product_id="prod-1",
            seller_id=seller_id,
        )
    )
    db.add(
        OrderPayment(
            order_id=order_code,
            payment_sequential=1,
            payment_type="credit_card",
            payment_installments=1,
            payment_value=100.0,
        )
    )
    db.commit()

    df = build_dataset(db)

    assert len(df) == 0


def test_multiple_payments_picks_highest_value(db: Session) -> None:
    customer_id = "cust-1"
    seller_id = "seller-1"
    db.add(Customer(customer_id=customer_id, customer_state="RJ"))
    db.add(Seller(seller_id=seller_id, seller_state="SP"))
    db.commit()

    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(
        db,
        customer_id=customer_id,
        estimated=estimated,
        actual=estimated,
        order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
    )
    db.add(Product(product_id="prod-1", weight_g=500, category_name_english="toys"))
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=1,
            product_id="prod-1",
            seller_id=seller_id,
        )
    )
    db.add(
        OrderPayment(
            order_id=order_code,
            payment_sequential=1,
            payment_type="voucher",
            payment_installments=1,
            payment_value=10.0,
        )
    )
    db.add(
        OrderPayment(
            order_id=order_code,
            payment_sequential=2,
            payment_type="credit_card",
            payment_installments=3,
            payment_value=90.0,
        )
    )
    db.commit()

    df = build_dataset(db)

    assert df[df["order_id"] == order_code]["payment_type"].iloc[0] == "credit_card"


def test_multiple_sellers_picks_first_order_item(db: Session) -> None:
    customer_id = "cust-1"
    db.add(Customer(customer_id=customer_id, customer_state="RJ"))
    db.add(Seller(seller_id="seller-first", seller_state="SP"))
    db.add(Seller(seller_id="seller-second", seller_state="PE"))
    db.commit()

    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(
        db,
        customer_id=customer_id,
        estimated=estimated,
        actual=estimated,
        order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
    )
    db.add(Product(product_id="prod-1", weight_g=500, category_name_english="toys"))
    db.add(Product(product_id="prod-2", weight_g=300, category_name_english="books"))
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=1,
            product_id="prod-1",
            seller_id="seller-first",
        )
    )
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=2,
            product_id="prod-2",
            seller_id="seller-second",
        )
    )
    db.add(
        OrderPayment(
            order_id=order_code,
            payment_sequential=1,
            payment_type="credit_card",
            payment_installments=1,
            payment_value=100.0,
        )
    )
    db.commit()

    df = build_dataset(db)

    assert df[df["order_id"] == order_code]["seller_state"].iloc[0] == "SP"


def test_order_weight_is_sum_of_all_items(db: Session) -> None:
    customer_id = "cust-1"
    seller_id = "seller-1"
    db.add(Customer(customer_id=customer_id, customer_state="RJ"))
    db.add(Seller(seller_id=seller_id, seller_state="SP"))
    db.commit()

    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(
        db,
        customer_id=customer_id,
        estimated=estimated,
        actual=estimated,
        order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
    )
    db.add(Product(product_id="prod-1", weight_g=500, category_name_english="toys"))
    db.add(Product(product_id="prod-2", weight_g=300, category_name_english="books"))
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=1,
            product_id="prod-1",
            seller_id=seller_id,
        )
    )
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=2,
            product_id="prod-2",
            seller_id=seller_id,
        )
    )
    db.add(
        OrderPayment(
            order_id=order_code,
            payment_sequential=1,
            payment_type="credit_card",
            payment_installments=1,
            payment_value=100.0,
        )
    )
    db.commit()

    df = build_dataset(db)

    assert df[df["order_id"] == order_code]["weight_g"].iloc[0] == 800


def test_category_picks_first_order_item(db: Session) -> None:
    customer_id = "cust-1"
    seller_id = "seller-1"
    db.add(Customer(customer_id=customer_id, customer_state="RJ"))
    db.add(Seller(seller_id=seller_id, seller_state="SP"))
    db.commit()

    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(
        db,
        customer_id=customer_id,
        estimated=estimated,
        actual=estimated,
        order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
    )
    db.add(Product(product_id="prod-1", weight_g=500, category_name_english="toys"))
    db.add(Product(product_id="prod-2", weight_g=300, category_name_english="books"))
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=1,
            product_id="prod-1",
            seller_id=seller_id,
        )
    )
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=2,
            product_id="prod-2",
            seller_id=seller_id,
        )
    )
    db.add(
        OrderPayment(
            order_id=order_code,
            payment_sequential=1,
            payment_type="credit_card",
            payment_installments=1,
            payment_value=100.0,
        )
    )
    db.commit()

    df = build_dataset(db)

    assert df[df["order_id"] == order_code]["category"].iloc[0] == "toys"


def test_order_missing_product_weight_excluded(db: Session) -> None:
    customer_id = "cust-1"
    seller_id = "seller-1"
    db.add(Customer(customer_id=customer_id, customer_state="RJ"))
    db.add(Seller(seller_id=seller_id, seller_state="SP"))
    db.commit()

    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(
        db,
        customer_id=customer_id,
        estimated=estimated,
        actual=estimated,
        order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
    )
    db.add(Product(product_id="prod-1", weight_g=None, category_name_english="toys"))
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=1,
            product_id="prod-1",
            seller_id=seller_id,
        )
    )
    db.add(
        OrderPayment(
            order_id=order_code,
            payment_sequential=1,
            payment_type="credit_card",
            payment_installments=1,
            payment_value=100.0,
        )
    )
    db.commit()

    df = build_dataset(db)

    assert len(df) == 0


def test_order_missing_product_category_excluded(db: Session) -> None:
    customer_id = "cust-1"
    seller_id = "seller-1"
    db.add(Customer(customer_id=customer_id, customer_state="RJ"))
    db.add(Seller(seller_id=seller_id, seller_state="SP"))
    db.commit()

    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(
        db,
        customer_id=customer_id,
        estimated=estimated,
        actual=estimated,
        order_purchase_timestamp=datetime(2024, 1, 1, tzinfo=UTC),
    )
    db.add(Product(product_id="prod-1", weight_g=500, category_name_english=None))
    db.add(
        OrderItem(
            order_id=order_code,
            order_item_id=1,
            product_id="prod-1",
            seller_id=seller_id,
        )
    )
    db.add(
        OrderPayment(
            order_id=order_code,
            payment_sequential=1,
            payment_type="credit_card",
            payment_installments=1,
            payment_value=100.0,
        )
    )
    db.commit()

    df = build_dataset(db)

    assert len(df) == 0


def test_split_train_test_ratio_and_no_overlap() -> None:
    df = pd.DataFrame(
        {
            "order_id": [f"order-{i}" for i in range(100)],
            "label": ["on_time"] * 100,
        }
    )

    train_df, test_df = split_train_test(df, test_size=0.2, random_state=42)

    assert len(train_df) == 80
    assert len(test_df) == 20
    assert set(train_df["order_id"]).isdisjoint(set(test_df["order_id"]))


def _clean_prepared_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": ["order-1", "order-2"],
            "seller_state": ["SP", "RJ"],
            "customer_state": ["RJ", "SP"],
            "payment_type": ["credit_card", "boleto"],
            "order_purchase_timestamp": [
                "2024-01-01T00:00:00+00:00",
                "2024-02-01T00:00:00+00:00",
            ],
            "weight_g": [500, 300],
            "category": ["toys", "books"],
            "label": ["on_time", "late"],
        }
    )


def test_data_quality_report_on_clean_data_reports_no_issues() -> None:
    df = _clean_prepared_dataframe()

    report = data_quality_report(df)

    assert all(pct == 0 for pct in report["missing_pct_by_column"].values())
    assert report["duplicate_order_ids"] == 0
    assert report["unexpected_labels"] == []
    assert report["unparseable_purchase_timestamps"] == 0


def test_data_quality_report_flags_missing_values() -> None:
    df = _clean_prepared_dataframe()
    df.loc[0, "weight_g"] = None

    report = data_quality_report(df)

    assert report["missing_pct_by_column"]["weight_g"] == 50.0


def test_data_quality_report_flags_duplicate_order_ids() -> None:
    df = _clean_prepared_dataframe()
    df.loc[1, "order_id"] = "order-1"

    report = data_quality_report(df)

    assert report["duplicate_order_ids"] == 1


def test_data_quality_report_flags_unexpected_labels() -> None:
    df = _clean_prepared_dataframe()
    df.loc[1, "label"] = "unknown"

    report = data_quality_report(df)

    assert report["unexpected_labels"] == ["unknown"]


def test_data_quality_report_flags_unparseable_timestamps() -> None:
    df = _clean_prepared_dataframe()
    df.loc[1, "order_purchase_timestamp"] = "not-a-date"

    report = data_quality_report(df)

    assert report["unparseable_purchase_timestamps"] == 1
