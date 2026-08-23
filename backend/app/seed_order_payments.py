import logging
from pathlib import Path

from sqlmodel import Session

from app.core.db import engine
from app.models import OrderPayment
from app.seed_utils import chunked_upsert, read_csv_rows

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "raw"
    / "olist_order_payments_dataset.csv"
)


def _map_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "order_id": row["order_id"],
        "payment_sequential": int(row["payment_sequential"]),
        "payment_type": row["payment_type"],
        "payment_installments": int(row["payment_installments"]),
        "payment_value": float(row["payment_value"]),
    }


def seed(session: Session, csv_path: Path = CSV_PATH) -> int:
    rows = read_csv_rows(csv_path, _map_row)
    return chunked_upsert(
        session,
        OrderPayment,
        rows,
        index_elements=["order_id", "payment_sequential"],
        update_columns=["payment_type", "payment_installments", "payment_value"],
    )


def main() -> None:
    logger.info("Seeding order payments from %s", CSV_PATH)
    with Session(engine) as session:
        count = seed(session)
    logger.info("Seeded/updated %d order payment rows", count)


if __name__ == "__main__":
    main()
