from datetime import UTC, datetime

from app.delivery import compute_delivery_status


def test_on_time_when_actual_same_date_but_later_time_of_day() -> None:
    estimated = datetime(2017, 10, 18, 0, 0, tzinfo=UTC)
    actual = datetime(2017, 10, 18, 23, 0, tzinfo=UTC)
    assert compute_delivery_status(estimated, actual) == "on_time"


def test_late_when_actual_date_is_after_estimated_date() -> None:
    estimated = datetime(2017, 10, 18, 0, 0, tzinfo=UTC)
    actual = datetime(2017, 10, 19, 0, 0, tzinfo=UTC)
    assert compute_delivery_status(estimated, actual) == "late"


def test_undetermined_when_actual_date_is_none() -> None:
    estimated = datetime(2017, 10, 18, 0, 0, tzinfo=UTC)
    assert compute_delivery_status(estimated, None) == "undetermined"
