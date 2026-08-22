"use server";

interface OrderLookupItem {
  product_category: string | null;
  seller_city: string | null;
  seller_state: string | null;
}

export interface OrderLookupResult {
  order_code: string;
  estimated_delivery_date: string;
  actual_delivery_date: string | null;
  status: "on_time" | "late" | "undetermined";
  items: OrderLookupItem[];
  customer_city: string | null;
  customer_state: string | null;
  customer_zip_code_prefix: string | null;
}

export type OrderLookupState =
  | { kind: "idle" }
  | { kind: "empty" }
  | { kind: "not_found"; code: string }
  | { kind: "error" }
  | { kind: "found"; data: OrderLookupResult };

export async function lookupOrder(
  _prevState: OrderLookupState,
  formData: FormData,
): Promise<OrderLookupState> {
  const code = String(formData.get("code") ?? "").trim();
  if (!code) {
    return { kind: "empty" };
  }

  const apiUrl = process.env.API_URL ?? "http://localhost:8000";
  const res = await fetch(`${apiUrl}/api/v1/orders/${encodeURIComponent(code)}`, {
    cache: "no-store",
  });

  if (res.status === 404) {
    return { kind: "not_found", code };
  }
  if (!res.ok) {
    return { kind: "error" };
  }

  const data: OrderLookupResult = await res.json();
  return { kind: "found", data };
}
