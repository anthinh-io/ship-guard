from collections.abc import Generator

import pytest
from sqlmodel import Session, delete

from app.core.db import engine
from app.models import Customer, Order, OrderItem, Product, Seller


@pytest.fixture
def db() -> Generator[Session]:
    with Session(engine) as session:
        _clear(session)
        session.commit()
        yield session
        _clear(session)
        session.commit()


def _clear(session: Session) -> None:
    session.execute(delete(OrderItem))
    session.execute(delete(Order))
    session.execute(delete(Product))
    session.execute(delete(Seller))
    session.execute(delete(Customer))
