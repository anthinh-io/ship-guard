import csv
import logging
import uuid
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session

from app.core.db import engine
from app.models import Order

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = (
    Path(__file__).resolve().parents[2] / "datasets" / "raw" / "olist_orders_dataset.csv"
)
CHUNK_SIZE = 1000


def _parse_utc(raw: str) -> datetime | None:
    if not raw:
        return None
    return datetime.strptime(raw, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)


def _read_rows(csv_path: Path) -> Iterator[dict[str, object]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield {
                "id": uuid.uuid4(),
                "order_code": row["order_id"],
                "estimated_delivery_date": _parse_utc(row["order_estimated_delivery_date"]),
                "actual_delivery_date": _parse_utc(row["order_delivered_customer_date"]),
                "processing_status": "Chưa xử lý",
            }


def _upsert_chunk(session: Session, chunk: list[dict[str, object]]) -> None:
    stmt = insert(Order).values(chunk)
    stmt = stmt.on_conflict_do_update(
        index_elements=[Order.order_code],
        set_={
            "estimated_delivery_date": stmt.excluded.estimated_delivery_date,
            "actual_delivery_date": stmt.excluded.actual_delivery_date,
        },
    )
    session.execute(stmt)
    session.commit()


def seed(session: Session, csv_path: Path = CSV_PATH) -> int:
    total = 0
    chunk: list[dict[str, object]] = []
    for row in _read_rows(csv_path):
        chunk.append(row)
        if len(chunk) >= CHUNK_SIZE:
            _upsert_chunk(session, chunk)
            total += len(chunk)
            chunk = []
    if chunk:
        _upsert_chunk(session, chunk)
        total += len(chunk)
    return total


def main() -> None:
    logger.info("Seeding orders from %s", CSV_PATH)
    with Session(engine) as session:
        count = seed(session)
    logger.info("Seeded/updated %d order rows", count)


if __name__ == "__main__":
    main()
