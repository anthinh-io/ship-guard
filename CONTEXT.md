# Ship Guard

Ứng dụng giám sát hiệu suất giao hàng và dự đoán rủi ro giao trễ, xây trên dữ liệu Olist (thương mại điện tử Brazil).

## Language

**Trạng thái giao hàng (Delivery status)**:
Một trong ba giá trị tính động từ `estimated_delivery_date` và `actual_delivery_date` của một đơn: đúng hạn (`on_time`) khi giao trong hoặc đúng ngày hẹn, trễ (`late`) khi giao sau ngày hẹn, chưa xác định (`undetermined`) khi chưa có ngày giao thực tế. Không lưu thành cột riêng trong CSDL — luôn tính lại qua hàm `compute_delivery_status`, so sánh theo ngày (bỏ giờ:phút:giây).
_Avoid_: "Trạng thái đơn hàng" (dễ nhầm với Trạng thái xử lý), `order_status` (tên cột gốc trong dữ liệu Olist, không dùng trực tiếp làm căn cứ)

**Trạng thái xử lý (Processing status)**:
Trạng thái vòng đời xử lý nghiệp vụ của một đơn hàng trong hệ thống (cột `processing_status` trên `Order`) — độc lập hoàn toàn với Trạng thái giao hàng. Giá trị mặc định khi tạo đơn là "Chưa xử lý".
_Avoid_: "Trạng thái đơn hàng" (mơ hồ, dễ nhầm với Trạng thái giao hàng)

**Đơn chưa xác định (Undetermined order)**:
Một đơn hàng chưa có `actual_delivery_date` (chưa giao xong) — bị loại khỏi mọi phép tính KPI đúng hạn/trễ và mọi nhãn huấn luyện, bất kể `order_status` gốc trong dữ liệu Olist là gì (xem [ADR 0001](docs/adr/0001-delivery-status-date-only-rule.md) về trường hợp ngoại lệ hiếm gặp).
_Avoid_: "Đơn đang xử lý", "Đơn treo"

**Nhãn rủi ro (Risk label)**:
Kết quả phân loại rủi ro trễ giao hàng cho một đơn, lưu trên cột `risk_label` của `Order` — một trong hai giá trị `high`/`low` (khoá tiếng Anh nội bộ). Dịch sang tiếng Việt lúc hiển thị: `high` → "Rủi ro cao", `low` → "Rủi ro thấp". `None` nghĩa là đơn chưa từng được dự đoán. Do luồng nhập đơn mới và nhận dự đoán rủi ro ghi vào; trang chi tiết đơn chỉ đọc và hiển thị.
_Avoid_: lưu thẳng chuỗi tiếng Việt "Rủi ro cao"/"Rủi ro thấp" vào cột này — tách dữ liệu khỏi câu chữ hiển thị, nhất quán với cách Trạng thái giao hàng đang được biểu diễn.

**Xác suất trễ (Risk probability)**:
Xác suất một đơn sẽ giao trễ, do mô hình dự đoán tính ra — lưu trên cột `risk_probability` của `Order`, dạng phân số 0.0–1.0 (không phải phần trăm). `None` khi đơn chưa có dự đoán.

**Thời điểm dự đoán (Predicted at)**:
Thời điểm mô hình thực hiện dự đoán cho một đơn — lưu trên cột `predicted_at` của `Order`. Chỉ lưu kết quả dự đoán gần nhất, không lưu lịch sử nhiều lần dự đoán.

**Hình thức thanh toán (Payment type)**:
Loại hình thanh toán của một đơn (vd. `credit_card`, `voucher`, `boleto`) — lưu trên bảng `OrderPayment`, mỗi đơn có thể có nhiều dòng thanh toán. Khi cần một giá trị đại diện duy nhất cho đơn (vd. để huấn luyện mô hình), chọn loại của dòng có `payment_value` cao nhất.

**Thời điểm đặt hàng (Order purchase timestamp)**:
Thời điểm khách đặt đơn hàng — lưu trên cột `order_purchase_timestamp` của `Order`.
