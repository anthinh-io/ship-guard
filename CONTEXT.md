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
