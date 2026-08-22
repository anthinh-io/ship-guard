import { OrderLookupForm } from "@/components/order-lookup-form";

export default function OrdersPage() {
  return (
    <main className="flex flex-1 flex-col items-center gap-8 p-16">
      <h1 className="text-2xl font-semibold">Tra cứu đơn hàng</h1>
      <OrderLookupForm />
    </main>
  );
}
