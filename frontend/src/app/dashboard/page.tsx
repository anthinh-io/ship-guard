import { DeliveryRateChart } from "@/components/delivery-rate-chart";

interface DashboardKpi {
  on_time_count: number;
  late_count: number;
  on_time_rate: number | null;
  late_rate: number | null;
}

export default async function DashboardPage() {
  const apiUrl = process.env.API_URL ?? "http://localhost:8000";
  const res = await fetch(`${apiUrl}/api/v1/dashboard/kpi`, {
    cache: "no-store",
  });

  if (!res.ok) {
    return (
      <main className="flex flex-1 items-center justify-center p-16">
        <p className="text-zinc-600 dark:text-zinc-400">
          Không thể tải dữ liệu KPI. Vui lòng thử lại sau.
        </p>
      </main>
    );
  }

  const kpi: DashboardKpi = await res.json();

  return (
    <main className="flex flex-1 flex-col items-center justify-center gap-8 p-16">
      <h1 className="text-2xl font-semibold">Tỷ lệ đúng hạn giao hàng</h1>
      <DeliveryRateChart
        onTimeCount={kpi.on_time_count}
        lateCount={kpi.late_count}
        onTimeRate={kpi.on_time_rate}
        lateRate={kpi.late_rate}
      />
    </main>
  );
}
