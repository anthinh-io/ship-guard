# Cách vận hành mô hình dự đoán rủi ro

**Serving**: hàm Python thuần `predict()` trong `backend/app/ml/predict.py`, chạy in-process ngay trong tiến trình FastAPI, model được load một lần lúc khởi động app. Không tách thành REST endpoint `/predict` riêng — #8 (luồng nhập đơn) gọi trực tiếp hàm này trong cùng process, không cần round-trip HTTP nội bộ.

**Training**: chạy thủ công qua CLI script `backend/app/ml/train_model.py` (cùng pattern với `prepare_training_data.py`). So sánh 3 thuật toán ([ADR 0002](0002-risk-model-algorithm-candidates.md)) bằng k-fold cross-validation (k=5) trên `train.csv`, xếp hạng theo recall lớp "trễ" — không chạm `test.csv` ở bước so sánh để tránh rò rỉ dữ liệu vào lựa chọn mô hình. Train lại thuật toán thắng cuộc trên toàn bộ `train.csv`, đo recall cuối cùng trên `test.csv` đúng một lần (ngưỡng pass > 30%). Chưa có kế hoạch tự động retrain định kỳ — quyết định tạm cho MVP, xem lại khi có luồng dữ liệu mới liên tục.

Recall đo được trên `test.csv` tại thời điểm implement (XGBoost thắng cuộc): **58.48%**.

**Đóng gói**: `joblib.dump()` model thắng cuộc vào `models/risk_model.joblib` ở root repo (cùng cấp với `datasets/`), commit vào git — theo đúng tiền lệ `datasets/processed/{train,test}.csv` đã commit.
