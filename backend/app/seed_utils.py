import csv
from collections.abc import Callable, Iterator
from pathlib import Path

from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, SQLModel


def read_csv_rows(
    csv_path: Path,
    mapper: Callable[[dict[str, str]], dict[str, object]],
    encoding: str = "utf-8-sig",
) -> Iterator[dict[str, object]]:
    with csv_path.open(newline="", encoding=encoding) as f:
        for row in csv.DictReader(f):
            yield mapper(row)


def chunked_upsert(
    session: Session,
    table: type[SQLModel],
    rows: Iterator[dict[str, object]],
    index_elements: list[str],
    update_columns: list[str],
    chunk_size: int = 1000,
) -> int:
    total = 0
    chunk: list[dict[str, object]] = []
    for row in rows:
        chunk.append(row)
        if len(chunk) >= chunk_size:
            total += _upsert_chunk(session, table, chunk, index_elements, update_columns)
            chunk = []
    if chunk:
        total += _upsert_chunk(session, table, chunk, index_elements, update_columns)
    return total


def _upsert_chunk(
    session: Session,
    table: type[SQLModel],
    chunk: list[dict[str, object]],
    index_elements: list[str],
    update_columns: list[str],
) -> int:
    stmt = insert(table).values(chunk)
    stmt = stmt.on_conflict_do_update(
        index_elements=index_elements,
        set_={col: getattr(stmt.excluded, col) for col in update_columns},
    )
    session.execute(stmt)
    session.commit()
    return len(chunk)
