from datetime import UTC, datetime
from typing import Literal

DeliveryStatus = Literal["on_time", "late", "undetermined"]


def compute_delivery_status(
    estimated_date: datetime, actual_date: datetime | None
) -> DeliveryStatus:
    if actual_date is None:
        return "undetermined"
    if actual_date.astimezone(UTC).date() <= estimated_date.astimezone(UTC).date():
        return "on_time"
    return "late"
