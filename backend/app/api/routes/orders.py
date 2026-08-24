from fastapi import APIRouter, HTTPException
from sqlmodel import col, select

from app.api.deps import SessionDep
from app.crud import create_order_with_prediction
from app.delivery import compute_delivery_status
from app.models import (
    Customer,
    Order,
    OrderCreate,
    OrderCreateResult,
    OrderItem,
    OrderLookupItem,
    OrderLookupResult,
    Product,
    Seller,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/categories")
def get_categories(session: SessionDep) -> list[str]:
    rows = session.exec(
        select(Product.category_name_english)
        .where(col(Product.category_name_english).is_not(None))
        .distinct()
        .order_by(col(Product.category_name_english))
    ).all()
    return [row for row in rows if row is not None]


@router.post("", status_code=201)
def create_order(order_create: OrderCreate, session: SessionDep) -> OrderCreateResult:
    order = create_order_with_prediction(session=session, order_create=order_create)
    assert order.risk_label is not None
    assert order.risk_probability is not None
    assert order.predicted_at is not None
    return OrderCreateResult(
        order_code=order.order_code,
        risk_label=order.risk_label,
        risk_probability=order.risk_probability,
        predicted_at=order.predicted_at,
    )


@router.get("/{code}")
def get_order(code: str, session: SessionDep) -> OrderLookupResult:
    order = session.exec(select(Order).where(Order.order_code == code)).first()
    if order is None:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy đơn hàng với mã này"
        )

    status = compute_delivery_status(
        order.estimated_delivery_date, order.actual_delivery_date
    )

    rows = session.exec(
        select(OrderItem, Product, Seller)
        .join(Product, OrderItem.product_id == Product.product_id, isouter=True)  # type: ignore[arg-type]
        .join(Seller, OrderItem.seller_id == Seller.seller_id, isouter=True)  # type: ignore[arg-type]
        .where(OrderItem.order_id == order.order_code)
    ).all()
    items = [
        OrderLookupItem(
            product_category=(
                (product.category_name_english or product.category_name)
                if product
                else None
            ),
            seller_city=seller.seller_city if seller else None,
            seller_state=seller.seller_state if seller else None,
        )
        for _, product, seller in rows
    ]

    customer = (
        session.get(Customer, order.customer_id)
        if order.customer_id is not None
        else None
    )

    return OrderLookupResult(
        order_code=order.order_code,
        estimated_delivery_date=order.estimated_delivery_date,
        actual_delivery_date=order.actual_delivery_date,
        status=status,
        items=items,
        customer_city=customer.customer_city if customer else None,
        customer_state=customer.customer_state if customer else None,
        customer_zip_code_prefix=customer.customer_zip_code_prefix if customer else None,
        risk_label=order.risk_label,
        risk_probability=order.risk_probability,
        predicted_at=order.predicted_at,
    )
