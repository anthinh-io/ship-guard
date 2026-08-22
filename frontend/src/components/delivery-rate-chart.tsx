"use client";

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

interface DeliveryRateChartProps {
  onTimeCount: number;
  lateCount: number;
  onTimeRate: number | null;
  lateRate: number | null;
}

const COLORS = { onTime: "#16a34a", late: "#dc2626" };

export function DeliveryRateChart({
  onTimeCount,
  lateCount,
  onTimeRate,
  lateRate,
}: DeliveryRateChartProps) {
  if (onTimeRate === null || lateRate === null) {
    return (
      <p className="text-zinc-600 dark:text-zinc-400">
        Chưa đủ dữ liệu để tính tỷ lệ đúng hạn.
      </p>
    );
  }

  const data = [
    { name: "Đúng hạn", value: onTimeCount, color: COLORS.onTime },
    { name: "Trễ", value: lateCount, color: COLORS.late },
  ];

  return (
    <div className="flex flex-col items-center gap-4">
      <div style={{ width: 320, height: 320 }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={70}
              outerRadius={110}
            >
              {data.map((entry) => (
                <Cell key={entry.name} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="flex gap-8 text-sm">
        <span>Đúng hạn: {(onTimeRate * 100).toFixed(1)}%</span>
        <span>Trễ: {(lateRate * 100).toFixed(1)}%</span>
      </div>
    </div>
  );
}
