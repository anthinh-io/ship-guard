import logging
from pathlib import Path

from sqlmodel import Session

from app.core.db import engine
from app.models import Seller
from app.seed_utils import chunked_upsert, read_csv_rows

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = (
    Path(__file__).resolve().parents[2] / "datasets" / "raw" / "olist_sellers_dataset.csv"
)


def _map_row(row: dict[str, str]) -> dict[str, object]:
    return {
        "seller_id": row["seller_id"],
        "seller_city": row["seller_city"] or None,
        "seller_state": row["seller_state"] or None,
    }


def seed(session: Session, csv_path: Path = CSV_PATH) -> int:
    rows = read_csv_rows(csv_path, _map_row)
    return chunked_upsert(
        session,
        Seller,
        rows,
        index_elements=["seller_id"],
        update_columns=["seller_city", "seller_state"],
    )


def main() -> None:
    logger.info("Seeding sellers from %s", CSV_PATH)
    with Session(engine) as session:
        count = seed(session)
    logger.info("Seeded/updated %d seller rows", count)


if __name__ == "__main__":
    main()
