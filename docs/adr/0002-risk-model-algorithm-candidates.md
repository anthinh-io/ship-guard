# Ba thuật toán ứng viên cho mô hình dự đoán rủi ro trễ giao

Khi xây mô hình dự đoán rủi ro trễ giao, huấn luyện và so sánh 3 thuật toán đại diện 3 họ khác nhau: **Logistic Regression** (linear), **Random Forest** (bagging), **XGBoost** (boosting) — thay vì chỉ dùng một thuật toán duy nhất. Chọn ra thuật toán tốt nhất theo recall trên lớp "trễ", đo bằng k-fold cross-validation trên tập train (không chạm tập test trong bước so sánh, để tránh rò rỉ dữ liệu vào lựa chọn mô hình).

XGBoost được chọn làm đại diện họ boosting thay vì `HistGradientBoostingClassifier` sẵn có trong scikit-learn.

## Considered Options

- `HistGradientBoostingClassifier` (scikit-learn, không cần thêm dependency) — không chọn, XGBoost được ưu tiên làm đại diện boosting.
