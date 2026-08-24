# Module này (backend/app/ml/) là ngoại lệ duy nhất cho phép dùng pandas/scikit-learn
# trong backend — phần seed/API còn lại vẫn không dùng pandas (xem docs/adr/0003-xgboost-dependency-placement.md).
import logging
from collections import defaultdict
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sqlmodel import Session, select

from app.core.db import engine
from app.delivery import compute_delivery_status
from app.models import Customer, Order, OrderItem, OrderPayment, Product, Seller

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).resolve().parents[3] / "datasets" / "processed"


def build_dataset(session: Session) -> pd.DataFrame:
    orders = session.exec(select(Order)).all()
    customers = {c.customer_id: c for c in session.exec(select(Customer)).all()}
    sellers = {s.seller_id: s for s in session.exec(select(Seller)).all()}
    products = {p.product_id: p for p in session.exec(select(Product)).all()}

    payments_by_order: dict[str, list[OrderPayment]] = defaultdict(list)
    for payment in session.exec(select(OrderPayment)).all():
        payments_by_order[payment.order_id].append(payment)

    items_by_order: dict[str, list[OrderItem]] = defaultdict(list)
    for item in session.exec(select(OrderItem)).all():
        items_by_order[item.order_id].append(item)

    rows: list[dict[str, object]] = []
    for order in orders:
        label = compute_delivery_status(
            order.estimated_delivery_date, order.actual_delivery_date
        )
        if label == "undetermined":
            continue

        customer = customers.get(order.customer_id) if order.customer_id else None
        customer_state = customer.customer_state if customer else None

        payments = payments_by_order.get(order.order_code, [])
        payment_type = (
            max(payments, key=lambda p: p.payment_value).payment_type
            if payments
            else None
        )

        items = sorted(
            items_by_order.get(order.order_code, []), key=lambda i: i.order_item_id
        )
        seller_state = None
        category = None
        if items:
            seller = sellers.get(items[0].seller_id)
            seller_state = seller.seller_state if seller else None
            first_product = products.get(items[0].product_id)
            category = first_product.category_name_english if first_product else None

        weight_g = None
        if items:
            resolved_weights: list[int] = []
            for item in items:
                product = products.get(item.product_id)
                if product is None or product.weight_g is None:
                    resolved_weights = []
                    break
                resolved_weights.append(product.weight_g)
            if resolved_weights:
                weight_g = sum(resolved_weights)

        if (
            seller_state is None
            or customer_state is None
            or payment_type is None
            or order.order_purchase_timestamp is None
            or weight_g is None
            or category is None
        ):
            continue

        rows.append(
            {
                "order_id": order.order_code,
                "seller_state": seller_state,
                "customer_state": customer_state,
                "payment_type": payment_type,
                "order_purchase_timestamp": order.order_purchase_timestamp,
                "weight_g": weight_g,
                "category": category,
                "label": label,
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "order_id",
            "seller_state",
            "customer_state",
            "payment_type",
            "order_purchase_timestamp",
            "weight_g",
            "category",
            "label",
        ],
    )


def split_train_test(
    df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_df, test_df = train_test_split(
        df, test_size=test_size, random_state=random_state
    )
    return train_df, test_df


def main() -> None:
    logger.info("Building training dataset from Postgres")
    with Session(engine) as session:
        df = build_dataset(session)
    logger.info("Built dataset with %d rows", len(df))

    train_df, test_df = split_train_test(df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(OUTPUT_DIR / "train.csv", index=False)
    test_df.to_csv(OUTPUT_DIR / "test.csv", index=False)
    logger.info(
        "Wrote %d train rows and %d test rows to %s",
        len(train_df),
        len(test_df),
        OUTPUT_DIR,
    )


if __name__ == "__main__":
    main()
