"use client";

import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import {
  orderFormSchema,
  type OrderFormValues,
  BRAZIL_STATES,
  PAYMENT_TYPES,
} from "@/app/orders/new/schema";
import { createOrder, type CreateOrderState } from "@/app/orders/new/actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";

const RISK_LABEL: Record<string, string> = { high: "Rủi ro cao", low: "Rủi ro thấp" };

const PAYMENT_LABEL: Record<string, string> = {
  boleto: "Boleto",
  credit_card: "Thẻ tín dụng",
  debit_card: "Thẻ ghi nợ",
  voucher: "Voucher",
};

function nowForDatetimeLocal(): string {
  const d = new Date();
  return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
}

export function OrderCreateForm({ categories }: { categories: string[] }) {
  const [result, setResult] = useState<CreateOrderState>({ kind: "idle" });
  const {
    register,
    handleSubmit,
    control,
    formState: { errors, isSubmitting },
  } = useForm<OrderFormValues>({
    resolver: zodResolver(orderFormSchema),
    defaultValues: { orderPurchaseTimestamp: nowForDatetimeLocal() },
  });

  async function onSubmit(values: OrderFormValues) {
    setResult(await createOrder(values));
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex w-full max-w-xl flex-col gap-4">
      <div className="flex flex-col gap-1">
        <label htmlFor="weightKg">Khối lượng (kg)</label>
        <Input
          id="weightKg"
          type="number"
          step="0.01"
          aria-invalid={!!errors.weightKg}
          {...register("weightKg")}
        />
        {errors.weightKg && (
          <p className="text-sm text-destructive">{errors.weightKg.message}</p>
        )}
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="category">Danh mục sản phẩm</label>
        <Controller
          name="category"
          control={control}
          render={({ field }) => (
            <Select onValueChange={field.onChange} value={field.value}>
              <SelectTrigger id="category" aria-invalid={!!errors.category}>
                <SelectValue placeholder="Chọn danh mục" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((c) => (
                  <SelectItem key={c} value={c}>
                    {c}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          )}
        />
        {errors.category && (
          <p className="text-sm text-destructive">{errors.category.message}</p>
        )}
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="paymentType">Phương thức thanh toán</label>
        <Controller
          name="paymentType"
          control={control}
          render={({ field }) => (
            <Select onValueChange={field.onChange} value={field.value}>
              <SelectTrigger id="paymentType" aria-invalid={!!errors.paymentType}>
                <SelectValue placeholder="Chọn phương thức" />
              </SelectTrigger>
              <SelectContent>
                {PAYMENT_TYPES.map((p) => (
                  <SelectItem key={p} value={p}>
                    {PAYMENT_LABEL[p]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          )}
        />
        {errors.paymentType && (
          <p className="text-sm text-destructive">{errors.paymentType.message}</p>
        )}
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="sellerState">Bang người bán</label>
        <Controller
          name="sellerState"
          control={control}
          render={({ field }) => (
            <Select onValueChange={field.onChange} value={field.value}>
              <SelectTrigger id="sellerState" aria-invalid={!!errors.sellerState}>
                <SelectValue placeholder="Chọn bang" />
              </SelectTrigger>
              <SelectContent>
                {BRAZIL_STATES.map((s) => (
                  <SelectItem key={s} value={s}>
                    {s}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          )}
        />
        {errors.sellerState && (
          <p className="text-sm text-destructive">{errors.sellerState.message}</p>
        )}
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="customerState">Bang khách hàng</label>
        <Controller
          name="customerState"
          control={control}
          render={({ field }) => (
            <Select onValueChange={field.onChange} value={field.value}>
              <SelectTrigger id="customerState" aria-invalid={!!errors.customerState}>
                <SelectValue placeholder="Chọn bang" />
              </SelectTrigger>
              <SelectContent>
                {BRAZIL_STATES.map((s) => (
                  <SelectItem key={s} value={s}>
                    {s}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          )}
        />
        {errors.customerState && (
          <p className="text-sm text-destructive">{errors.customerState.message}</p>
        )}
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="orderPurchaseTimestamp">Thời gian đặt hàng</label>
        <Input
          id="orderPurchaseTimestamp"
          type="datetime-local"
          aria-invalid={!!errors.orderPurchaseTimestamp}
          {...register("orderPurchaseTimestamp")}
        />
        {errors.orderPurchaseTimestamp && (
          <p className="text-sm text-destructive">{errors.orderPurchaseTimestamp.message}</p>
        )}
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="estimatedDeliveryDate">Ngày giao dự kiến</label>
        <Input
          id="estimatedDeliveryDate"
          type="datetime-local"
          aria-invalid={!!errors.estimatedDeliveryDate}
          {...register("estimatedDeliveryDate")}
        />
        {errors.estimatedDeliveryDate && (
          <p className="text-sm text-destructive">{errors.estimatedDeliveryDate.message}</p>
        )}
      </div>

      <Button type="submit" disabled={isSubmitting}>
        Tạo đơn hàng
      </Button>

      {result.kind === "error" && (
        <p className="text-sm text-zinc-600 dark:text-zinc-400">
          Không thể tạo đơn hàng. Vui lòng kiểm tra lại thông tin và thử lại.
        </p>
      )}

      {result.kind === "success" && (
        <div className="flex flex-col gap-2 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
          <p className="text-sm text-zinc-600 dark:text-zinc-400">
            Đã tạo đơn hàng {result.data.order_code}
          </p>
          <p className="text-sm text-zinc-600 dark:text-zinc-400">
            {RISK_LABEL[result.data.risk_label]} ({Math.round(result.data.risk_probability * 100)}%)
          </p>
        </div>
      )}
    </form>
  );
}
