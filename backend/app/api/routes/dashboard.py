from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import SessionDep
from app.delivery import compute_delivery_status
from app.models import DashboardKpi, Order

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/kpi")
def get_kpi(session: SessionDep) -> DashboardKpi:
    rows = session.exec(
        select(Order.estimated_delivery_date, Order.actual_delivery_date)
    ).all()

    on_time_count = 0
    late_count = 0
    for estimated, actual in rows:
        status = compute_delivery_status(estimated, actual)
        if status == "on_time":
            on_time_count += 1
        elif status == "late":
            late_count += 1

    considered_count = on_time_count + late_count
    if considered_count == 0:
        return DashboardKpi(
            on_time_count=0, late_count=0, on_time_rate=None, late_rate=None
        )

    return DashboardKpi(
        on_time_count=on_time_count,
        late_count=late_count,
        on_time_rate=on_time_count / considered_count,
        late_rate=late_count / considered_count,
    )
