# Ngưỡng 50% cho Nhãn rủi ro cao/thấp

Đơn được xếp "rủi ro cao" khi Xác suất trễ do model dự đoán > 50%, ngược lại "rủi ro thấp". 50% là điểm giữa tự nhiên của xác suất nhị phân — chọn làm mốc khởi điểm vì chưa có dữ liệu vận hành thật (vd. chi phí can thiệp nhầm so với chi phí bỏ lỡ một đơn trễ) để tinh chỉnh khác đi.

Đáng lưu ý: tập huấn luyện lệch lớp mạnh (~7% đơn trễ, xem [ADR 0002](0002-risk-model-algorithm-candidates.md)) — một ngưỡng thấp hơn 50% có thể bắt được nhiều đơn trễ hơn, nhưng chưa có cơ sở thực tế nào để chọn con số cụ thể khác. Xem lại ngưỡng này khi có phản hồi vận hành thật.
