import logging
from pathlib import Path

from sqlmodel import Session

from app.core.db import engine
from app.models import Product
from app.seed_utils import chunked_upsert, read_csv_rows

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CSV_PATH = (
    Path(__file__).resolve().parents[2] / "datasets" / "raw" / "olist_products_dataset.csv"
)
TRANSLATION_CSV_PATH = (
    Path(__file__).resolve().parents[2]
    / "datasets"
    / "raw"
    / "product_category_name_translation.csv"
)


def _load_translations(csv_path: Path) -> dict[str, str]:
    translations: dict[str, str] = {}
    for row in read_csv_rows(
        csv_path,
        lambda r: {
            "pt": r["product_category_name"],
            "en": r["product_category_name_english"],
        },
    ):
        translations[str(row["pt"])] = str(row["en"])
    return translations


def _map_row(row: dict[str, str], translations: dict[str, str]) -> dict[str, object]:
    category_name = row["product_category_name"] or None
    return {
        "product_id": row["product_id"],
        "category_name": category_name,
        "category_name_english": translations.get(category_name, category_name)
        if category_name
        else None,
    }


def seed(
    session: Session,
    csv_path: Path = CSV_PATH,
    translation_csv_path: Path = TRANSLATION_CSV_PATH,
) -> int:
    translations = _load_translations(translation_csv_path)
    rows = read_csv_rows(csv_path, lambda r: _map_row(r, translations))
    return chunked_upsert(
        session,
        Product,
        rows,
        index_elements=["product_id"],
        update_columns=["category_name", "category_name_english"],
    )


def main() -> None:
    logger.info("Seeding products from %s", CSV_PATH)
    with Session(engine) as session:
        count = seed(session)
    logger.info("Seeded/updated %d product rows", count)


if __name__ == "__main__":
    main()
