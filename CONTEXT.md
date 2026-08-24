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
Kết quả phân loại rủi ro trễ giao hàng cho một đơn, lưu trên cột `risk_label` của `Order` — một trong hai giá trị `high`/`low` (khoá tiếng Anh nội bộ). `high` khi Xác suất trễ > 50%, ngược lại `low` (xem [ADR 0004](docs/adr/0004-risk-threshold-50-percent.md) về lý do chọn 50%). Dịch sang tiếng Việt lúc hiển thị: `high` → "Rủi ro cao", `low` → "Rủi ro thấp". `None` nghĩa là đơn chưa từng được dự đoán. Do luồng nhập đơn mới và nhận dự đoán rủi ro ghi vào; trang chi tiết đơn chỉ đọc và hiển thị.
_Avoid_: lưu thẳng chuỗi tiếng Việt "Rủi ro cao"/"Rủi ro thấp" vào cột này — tách dữ liệu khỏi câu chữ hiển thị, nhất quán với cách Trạng thái giao hàng đang được biểu diễn.

**Xác suất trễ (Risk probability)**:
Xác suất một đơn sẽ giao trễ, do mô hình dự đoán tính ra — lưu trên cột `risk_probability` của `Order`, dạng phân số 0.0–1.0 (không phải phần trăm). `None` khi đơn chưa có dự đoán.

**Thời điểm dự đoán (Predicted at)**:
Thời điểm mô hình thực hiện dự đoán cho một đơn — lưu trên cột `predicted_at` của `Order`. Chỉ lưu kết quả dự đoán gần nhất, không lưu lịch sử nhiều lần dự đoán.

**Hình thức thanh toán (Payment type)**:
Loại hình thanh toán của một đơn (vd. `credit_card`, `voucher`, `boleto`). Với Đơn lịch sử: lưu trên bảng `OrderPayment`, mỗi đơn có thể có nhiều dòng thanh toán — khi cần một giá trị đại diện duy nhất (vd. để huấn luyện mô hình), chọn loại của dòng có `payment_value` cao nhất. Với Đơn mới: nhân viên chọn trực tiếp, lưu thẳng vào cột `payment_type` của `Order` (xem [ADR 0006](docs/adr/0006-new-order-features-flat-on-order.md)).

**Thời điểm đặt hàng (Order purchase timestamp)**:
Thời điểm khách đặt đơn hàng — lưu trên cột `order_purchase_timestamp` của `Order`. Với Đơn mới, mặc định là thời điểm nhân viên mở biểu mẫu, có thể sửa lại.

**Đơn lịch sử (Historical order)**:
Một đơn hàng import từ dữ liệu Olist gốc, dùng làm dữ liệu huấn luyện mô hình. Cân nặng/danh mục/hình thức thanh toán/vùng người bán/vùng người mua của loại đơn này suy ra qua join với `Product`/`OrderItem`/`OrderPayment`/`Seller`/`Customer`, không lưu trực tiếp trên `Order`.
_Avoid_: "Đơn cũ" (mơ hồ, không nói rõ là dữ liệu import)

**Đơn mới (New order)**:
Một đơn hàng do nhân viên vận hành tự nhập qua biểu mẫu nhập đơn, để nhận dự đoán rủi ro ngay. Cân nặng, danh mục, hình thức thanh toán, vùng người bán, vùng người mua của loại đơn này lưu trực tiếp trên `Order` (cột `weight_g`, `category`, `payment_type`, `seller_state`, `customer_state`) — không tạo kèm `Customer`/`Seller`/`Product`/`OrderItem`/`OrderPayment` như Đơn lịch sử (xem [ADR 0006](docs/adr/0006-new-order-features-flat-on-order.md)). Phân biệt Đơn mới với Đơn lịch sử bằng việc 5 cột này có giá trị hay không — không có cột đánh dấu loại đơn riêng.
_Avoid_: "Đơn nhập tay" (không phải thuật ngữ chính thức)

**Cân nặng đơn (Order weight)**:
Tổng cân nặng (gram) của một đơn hàng, dùng làm đặc trưng dự đoán rủi ro. Với Đơn lịch sử: tổng `weight_g` của tất cả sản phẩm (`Product`) trong đơn qua `OrderItem`. Với Đơn mới: nhân viên nhập bằng kilogram trên biểu mẫu, quy đổi sang gram trước khi lưu vào cột `weight_g` của `Order`.

**Danh mục (Category)**:
Danh mục sản phẩm của một đơn hàng, dùng làm đặc trưng dự đoán rủi ro. Với Đơn lịch sử: `category_name_english` của sản phẩm thuộc `OrderItem` có `order_item_id` nhỏ nhất. Với Đơn mới: nhân viên chọn từ danh sách danh mục thật đã có trong `Product`, lưu trực tiếp vào cột `category` của `Order`.

**Vùng người bán / Vùng người mua (Seller state / Customer state)**:
Mã bang Brazil (2 ký tự) nơi người bán gửi hàng / nơi người mua nhận hàng, dùng làm đặc trưng dự đoán rủi ro. Với Đơn lịch sử: `seller_state` của `Seller` (qua `OrderItem` có `order_item_id` nhỏ nhất) / `customer_state` của `Customer` (qua `Order.customer_id`). Với Đơn mới: nhân viên chọn từ đủ 27 mã bang Brazil, lưu trực tiếp vào cột `seller_state`/`customer_state` của `Order` — không giới hạn theo các bang đã từng xuất hiện trong dữ liệu lịch sử.
