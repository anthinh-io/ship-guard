import uuid
from datetime import UTC, datetime

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.models import Customer, Order, OrderItem, Product, Seller

client = TestClient(app)


def _make_order(
    session: Session,
    *,
    order_code: str | None = None,
    customer_id: str | None = None,
    estimated: datetime,
    actual: datetime | None,
    risk_label: str | None = None,
    risk_probability: float | None = None,
    predicted_at: datetime | None = None,
) -> str:
    order_code = order_code or f"test-{uuid.uuid4().hex}"
    order = Order(
        order_code=order_code,
        customer_id=customer_id,
        estimated_delivery_date=estimated,
        actual_delivery_date=actual,
        risk_label=risk_label,
        risk_probability=risk_probability,
        predicted_at=predicted_at,
    )
    session.add(order)
    session.commit()
    return order_code


def test_lookup_found_with_full_data(db: Session) -> None:
    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    customer = Customer(
        customer_id="cust-1", customer_city="sao paulo", customer_state="SP",
        customer_zip_code_prefix="01000",
    )
    product = Product(
        product_id="prod-1", category_name="beleza_saude",
        category_name_english="health_beauty",
    )
    seller = Seller(seller_id="seller-1", seller_city="campinas", seller_state="SP")
    db.add(customer)
    db.add(product)
    db.add(seller)
    db.commit()

    order_code = _make_order(
        db, customer_id="cust-1", estimated=estimated, actual=estimated
    )
    db.add(
        OrderItem(
            order_id=order_code, order_item_id=1, product_id="prod-1", seller_id="seller-1"
        )
    )
    db.commit()

    response = client.get(f"/api/v1/orders/{order_code}")

    assert response.status_code == 200
    data = response.json()
    assert data["order_code"] == order_code
    assert data["status"] == "on_time"
    assert data["items"] == [
        {"product_category": "health_beauty", "seller_city": "campinas", "seller_state": "SP"}
    ]
    assert data["customer_city"] == "sao paulo"
    assert data["customer_state"] == "SP"
    assert data["customer_zip_code_prefix"] == "01000"


def test_lookup_not_found(db: Session) -> None:
    assert db.exec(select(Order)).first() is None

    response = client.get("/api/v1/orders/does-not-exist")

    assert response.status_code == 404


def test_lookup_undetermined_when_no_actual_date(db: Session) -> None:
    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(db, estimated=estimated, actual=None)

    response = client.get(f"/api/v1/orders/{order_code}")

    assert response.status_code == 200
    assert response.json()["status"] == "undetermined"


def test_lookup_returns_all_items_for_multi_item_order(db: Session) -> None:
    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    db.add(Product(product_id="prod-1", category_name="informatica_acessorios"))
    db.add(Product(product_id="prod-2", category_name="perfumaria"))
    db.add(Seller(seller_id="seller-1", seller_city="campinas", seller_state="SP"))
    db.add(Seller(seller_id="seller-2", seller_city="recife", seller_state="PE"))
    db.commit()

    order_code = _make_order(db, estimated=estimated, actual=estimated)
    db.add(
        OrderItem(
            order_id=order_code, order_item_id=1, product_id="prod-1", seller_id="seller-1"
        )
    )
    db.add(
        OrderItem(
            order_id=order_code, order_item_id=2, product_id="prod-2", seller_id="seller-2"
        )
    )
    db.commit()

    response = client.get(f"/api/v1/orders/{order_code}")

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 2
    sellers = {item["seller_city"] for item in items}
    assert sellers == {"campinas", "recife"}


def test_lookup_order_with_no_items_returns_empty_list(db: Session) -> None:
    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(db, estimated=estimated, actual=estimated)

    response = client.get(f"/api/v1/orders/{order_code}")

    assert response.status_code == 200
    assert response.json()["items"] == []


def test_lookup_order_with_no_customer_returns_null_address(db: Session) -> None:
    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(db, customer_id=None, estimated=estimated, actual=estimated)

    response = client.get(f"/api/v1/orders/{order_code}")

    assert response.status_code == 200
    data = response.json()
    assert data["customer_city"] is None
    assert data["customer_state"] is None
    assert data["customer_zip_code_prefix"] is None


def test_lookup_order_with_saved_prediction_returns_risk_fields(db: Session) -> None:
    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    predicted_at = datetime(2024, 1, 5, tzinfo=UTC)
    order_code = _make_order(
        db,
        estimated=estimated,
        actual=estimated,
        risk_label="high",
        risk_probability=0.73,
        predicted_at=predicted_at,
    )

    response = client.get(f"/api/v1/orders/{order_code}")

    assert response.status_code == 200
    data = response.json()
    assert data["risk_label"] == "high"
    assert data["risk_probability"] == 0.73
    assert data["predicted_at"] is not None


def test_lookup_order_without_prediction_returns_null_risk_fields(db: Session) -> None:
    estimated = datetime(2024, 1, 10, tzinfo=UTC)
    order_code = _make_order(db, estimated=estimated, actual=estimated)

    response = client.get(f"/api/v1/orders/{order_code}")

    assert response.status_code == 200
    data = response.json()
    assert data["risk_label"] is None
    assert data["risk_probability"] is None
    assert data["predicted_at"] is None
