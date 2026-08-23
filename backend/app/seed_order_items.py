import logging
from pathlib import Path

from sqlmodel import Session

from app.core.db import engine
from app.models import OrderItem
from app.seed_utils import chunked_upsert, read_csv_rows

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = (
    Path(__file__).resolve().parents[2] / "datasets" / "raw" / "olist_order_items_dataset.csv"
)


def _map_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "order_id": row["order_id"],
        "order_item_id": int(row["order_item_id"]),
        "product_id": row["product_id"],
        "seller_id": row["seller_id"],
    }


def seed(session: Session, csv_path: Path = CSV_PATH) -> int:
    rows = read_csv_rows(csv_path, _map_row)
    return chunked_upsert(
        session,
        OrderItem,
        rows,
        index_elements=["order_id", "order_item_id"],
        update_columns=["product_id", "seller_id"],
    )


def main() -> None:
    logger.info("Seeding order items from %s", CSV_PATH)
    with Session(engine) as session:
        count = seed(session)
    logger.info("Seeded/updated %d order item rows", count)


if __name__ == "__main__":
    main()
