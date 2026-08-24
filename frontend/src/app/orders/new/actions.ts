"use server";

import { orderFormSchema, type OrderFormValues } from "./schema";

export interface OrderCreateResult {
  order_code: string;
  risk_label: "high" | "low";
  risk_probability: number;
  predicted_at: string;
}

export type CreateOrderState =
  | { kind: "idle" }
  | { kind: "error" }
  | { kind: "success"; data: OrderCreateResult };

export async function createOrder(values: OrderFormValues): Promise<CreateOrderState> {
  const parsed = orderFormSchema.safeParse(values);
  if (!parsed.success) {
    return { kind: "error" };
  }

  const apiUrl = process.env.API_URL ?? "http://localhost:8000";
  const res = await fetch(`${apiUrl}/api/v1/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    body: JSON.stringify({
      weight_g: Math.round(Number(parsed.data.weightKg) * 1000),
      category: parsed.data.category,
      payment_type: parsed.data.paymentType,
      seller_state: parsed.data.sellerState,
      customer_state: parsed.data.customerState,
      order_purchase_timestamp: new Date(parsed.data.orderPurchaseTimestamp).toISOString(),
      estimated_delivery_date: new Date(parsed.data.estimatedDeliveryDate).toISOString(),
    }),
  });

  if (!res.ok) {
    return { kind: "error" };
  }

  const data: OrderCreateResult = await res.json();
  return { kind: "success", data };
}
