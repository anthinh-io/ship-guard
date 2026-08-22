from collections.abc import Generator

import pytest
from sqlmodel import Session, delete

from app.core.db import engine
from app.models import Order


@pytest.fixture
def db() -> Generator[Session]:
    with Session(engine) as session:
        session.execute(delete(Order))
        session.commit()
        yield session
        session.execute(delete(Order))
        session.commit()
