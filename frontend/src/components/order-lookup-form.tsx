"use client";

import { useActionState } from "react";

import { lookupOrder, type OrderLookupState } from "@/app/orders/actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const STATUS_LABEL: Record<string, string> = {
  on_time: "Đúng hạn",
  late: "Trễ",
  undetermined: "Chưa xác định",
};

const initialState: OrderLookupState = { kind: "idle" };

export function OrderLookupForm() {
  const [state, formAction, pending] = useActionState(lookupOrder, initialState);

  return (
    <div className="flex w-full max-w-xl flex-col gap-6">
      <form action={formAction} className="flex gap-2">
        <Input name="code" placeholder="Nhập mã đơn hàng" required />
        <Button type="submit" disabled={pending}>
          Tra cứu
        </Button>
      </form>

      {state.kind === "empty" && (
        <p className="text-zinc-600 dark:text-zinc-400">Vui lòng nhập mã đơn hàng.</p>
      )}

      {state.kind === "not_found" && (
        <p className="text-zinc-600 dark:text-zinc-400">
          Không tìm thấy đơn hàng với mã &quot;{state.code}&quot;.
        </p>
      )}

      {state.kind === "error" && (
        <p className="text-zinc-600 dark:text-zinc-400">
          Không thể tra cứu đơn hàng. Vui lòng thử lại sau.
        </p>
      )}

      {state.kind === "found" && (
        <div className="flex flex-col gap-4 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
          <div>
            <p className="font-semibold">{state.data.order_code}</p>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">
              Ngày giao dự kiến: {state.data.estimated_delivery_date.slice(0, 10)}
              {state.data.actual_delivery_date &&
                ` · Ngày giao thực tế: ${state.data.actual_delivery_date.slice(0, 10)}`}
            </p>
            <p className="text-sm font-medium">
              Trạng thái: {STATUS_LABEL[state.data.status]}
            </p>
          </div>

          <div>
            <p className="font-medium">Sản phẩm</p>
            {state.data.items.length === 0 ? (
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                Không có thông tin sản phẩm.
              </p>
            ) : (
              <ul className="list-disc pl-5 text-sm">
                {state.data.items.map((item, i) => (
                  <li key={i}>
                    {item.product_category ?? "Không rõ danh mục"}
                    {" — "}
                    {item.seller_city
                      ? `${item.seller_city}, ${item.seller_state}`
                      : "Không rõ người bán"}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div>
            <p className="font-medium">Địa chỉ giao</p>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">
              {state.data.customer_city
                ? `${state.data.customer_city}, ${state.data.customer_state} - ${state.data.customer_zip_code_prefix}`
                : "Không có thông tin địa chỉ"}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
