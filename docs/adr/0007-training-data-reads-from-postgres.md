# Dữ liệu huấn luyện đọc từ Postgres, không đọc trực tiếp CSV gốc

`build_dataset()` (`backend/app/ml/prepare_training_data.py`) đọc dữ liệu đơn hàng qua SQLModel/Postgres (dữ liệu đã seed từ Story #1–4), không đọc trực tiếp `datasets/raw/*.csv`.

Lý do: đọc qua Postgres cho phép tái dùng đúng hàm `compute_delivery_status` và các model đã có sẵn (`Order`, `OrderItem`, `Seller`, `Customer`, `OrderPayment`), làm việc trực tiếp trên dữ liệu đã parse thay vì viết lại logic đọc/parse CSV riêng; đồng thời tận dụng dữ liệu đã seed sẵn, tránh hai pipeline nạp dữ liệu song song có thể lệch nhau.

Quyết định này đã chốt từ spec gốc của Story #6 (mục Solution trong comment spec trên issue #6: "đọc dữ liệu đơn hàng từ Postgres") — sub-issue #22/#27 (tạo trước hoặc độc lập với spec đó) mô tả phương án đọc trực tiếp CSV, chưa từng được cập nhật theo quyết định thật.
