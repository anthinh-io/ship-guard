# ADR 0001: Trạng thái giao hàng so sánh theo ngày, bỏ qua order_status gốc

## Bối cảnh

`compute_delivery_status(estimated_date, actual_date)` cần một quy tắc duy nhất, tính động, để
phân loại mọi đơn hàng thành đúng hạn / trễ / chưa xác định, dùng chung cho KPI dashboard và (sau
này) nhãn huấn luyện mô hình dự đoán.

## Quyết định

1. So sánh chỉ theo **ngày** (bỏ giờ:phút:giây) của `estimated_delivery_date` và
   `actual_delivery_date`. Giao đúng ngày hẹn hoặc sớm hơn → `on_time`; giao sau ngày hẹn →
   `late`.
2. `actual_delivery_date` là `None` → luôn luôn `undetermined`, không có logic nghiệp vụ nào khác
   can thiệp.
3. Trường `order_status` gốc trong dữ liệu Olist **không được dùng** làm căn cứ, kể cả khi có mâu
   thuẫn: dữ liệu thô có khoảng 6 đơn `canceled` vẫn có ngày giao thực tế, và khoảng 8 đơn
   `delivered` lại thiếu ngày giao thực tế. Đây là điểm nhiễu đã biết của bộ dữ liệu Olist, được
   chấp nhận như một hạn chế đã ghi nhận, không xử lý ngoại lệ riêng cho từng trường hợp.

## Hệ quả

- Toàn bộ 99.441 dòng của `olist_orders_dataset.csv` được nạp vào bảng `orders`, không lọc theo
  `order_status` — chỉ `actual_delivery_date` (null hay không) quyết định một đơn có "chưa xác
  định" hay không.
- Nếu về sau phát hiện điểm nhiễu này ảnh hưởng đáng kể đến độ chính xác của mô hình dự đoán hoặc
  gây hiểu nhầm trên dashboard, cần một ADR mới để thay đổi quy tắc — không sửa ngầm trong
  `compute_delivery_status` mà không ghi lại quyết định.
