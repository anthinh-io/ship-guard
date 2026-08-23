import logging
import uuid
from datetime import UTC, datetime
from pathlib import Path

from sqlmodel import Session

from app.core.db import engine
from app.models import Order
from app.seed_utils import chunked_upsert, read_csv_rows

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = (
    Path(__file__).resolve().parents[2] / "datasets" / "raw" / "olist_orders_dataset.csv"
)


def _parse_utc(raw: str) -> datetime | None:
    if not raw:
        return None
    return datetime.strptime(raw, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC)


def _map_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "id": uuid.uuid4(),
        "order_code": row["order_id"],
        "customer_id": row["customer_id"],
        "estimated_delivery_date": _parse_utc(row["order_estimated_delivery_date"]),
        "actual_delivery_date": _parse_utc(row["order_delivered_customer_date"]),
        "order_purchase_timestamp": _parse_utc(row["order_purchase_timestamp"]),
        "processing_status": "Chưa xử lý",
    }


def seed(session: Session, csv_path: Path = CSV_PATH) -> int:
    rows = read_csv_rows(csv_path, _map_row)
    return chunked_upsert(
        session,
        Order,
        rows,
        index_elements=["order_code"],
        update_columns=[
            "customer_id",
            "estimated_delivery_date",
            "actual_delivery_date",
            "order_purchase_timestamp",
        ],
    )


def main() -> None:
    logger.info("Seeding orders from %s", CSV_PATH)
    with Session(engine) as session:
        count = seed(session)
    logger.info("Seeded/updated %d order rows", count)


if __name__ == "__main__":
    main()
