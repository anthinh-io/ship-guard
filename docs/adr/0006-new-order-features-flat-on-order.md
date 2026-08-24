# Đặc trưng dự đoán của đơn mới lưu trực tiếp trên Order, không tái dùng schema lịch sử

Đơn tạo qua biểu mẫu nhập đơn mới (nhân viên vận hành tự gõ) lưu 5 giá trị đầu vào cho mô hình dự đoán — cân nặng, danh mục, hình thức thanh toán, vùng người bán, vùng người mua — trực tiếp thành 5 cột mới trên `Order` (`weight_g`, `category`, `payment_type`, `seller_state`, `customer_state`, tất cả nullable), thay vì tạo kèm `Customer`/`Seller`/`Product`/`OrderItem`/`OrderPayment` như cách dữ liệu lịch sử Olist được tổ chức.

Lý do: hàm `predict()` (#7) đã nhận đúng 6 giá trị vô hướng này (`OrderFeatures`), không cần tham chiếu entity. Nhân viên tạo đơn mới cũng không có `seller_id`/`product_id` nào để chọn — AC mô tả các trường này như giá trị nhập trực tiếp. Các bảng quan hệ lịch sử giữ nguyên vai trò chỉ phục vụ dữ liệu Olist gốc dùng để huấn luyện, không mở rộng cho đơn mới.

Đơn lịch sử (import từ Olist) để trống 5 cột này — không backfill.
