import { OrderCreateForm } from "@/components/order-create-form";

async function getCategories(): Promise<string[]> {
  const apiUrl = process.env.API_URL ?? "http://localhost:8000";
  const res = await fetch(`${apiUrl}/api/v1/orders/categories`, { cache: "no-store" });
  if (!res.ok) {
    return [];
  }
  return res.json();
}

export default async function NewOrderPage() {
  const categories = await getCategories();

  return (
    <main className="flex flex-col items-center gap-6 p-8">
      <h1 className="text-xl font-semibold">Tạo đơn hàng mới</h1>
      <OrderCreateForm categories={categories} />
    </main>
  );
}
