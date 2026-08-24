import { z } from "zod";

// Keep in sync with BrazilState in backend/app/models.py
export const BRAZIL_STATES = [
  "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
  "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
] as const;

// Keep in sync with PaymentType in backend/app/models.py
export const PAYMENT_TYPES = ["boleto", "credit_card", "debit_card", "voucher"] as const;

export const orderFormSchema = z.object({
  weightKg: z
    .string()
    .min(1, "Vui lòng nhập khối lượng.")
    .refine((v) => Number(v) > 0, "Khối lượng phải lớn hơn 0."),
  category: z.string().min(1, "Vui lòng chọn danh mục sản phẩm."),
  paymentType: z.enum(PAYMENT_TYPES, { error: "Vui lòng chọn phương thức thanh toán." }),
  sellerState: z.enum(BRAZIL_STATES, { error: "Vui lòng chọn bang người bán." }),
  customerState: z.enum(BRAZIL_STATES, { error: "Vui lòng chọn bang khách hàng." }),
  orderPurchaseTimestamp: z.string().min(1, "Vui lòng nhập thời gian đặt hàng."),
  estimatedDeliveryDate: z.string().min(1, "Vui lòng nhập ngày giao dự kiến."),
});

export type OrderFormValues = z.infer<typeof orderFormSchema>;
