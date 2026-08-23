import logging
from pathlib import Path

from sqlmodel import Session

from app.core.db import engine
from app.models import Customer
from app.seed_utils import chunked_upsert, read_csv_rows

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = (
    Path(__file__).resolve().parents[2] / "datasets" / "raw" / "olist_customers_dataset.csv"
)


def _map_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "customer_id": row["customer_id"],
        "customer_city": row["customer_city"] or None,
        "customer_state": row["customer_state"] or None,
        "customer_zip_code_prefix": row["customer_zip_code_prefix"] or None,
    }


def seed(session: Session, csv_path: Path = CSV_PATH) -> int:
    rows = read_csv_rows(csv_path, _map_row)
    return chunked_upsert(
        session,
        Customer,
        rows,
        index_elements=["customer_id"],
        update_columns=[
            "customer_city",
            "customer_state",
            "customer_zip_code_prefix",
        ],
    )


def main() -> None:
    logger.info("Seeding customers from %s", CSV_PATH)
    with Session(engine) as session:
        count = seed(session)
    logger.info("Seeded/updated %d customer rows", count)


if __name__ == "__main__":
    main()
