# `xgboost` khai báo trong `backend/pyproject.toml`, không phải root

`backend/app/ml/predict()` gọi model đã huấn luyện ngay trong tiến trình FastAPI lúc phục vụ request (in-process, không tách service riêng). Nếu XGBoost là thuật toán thắng cuộc (xem [ADR 0002](0002-risk-model-algorithm-candidates.md)), `xgboost` trở thành dependency runtime thật của API, không chỉ dùng lúc huấn luyện — nên vẫn khai báo trong `backend/pyproject.toml` cùng nhóm với `pandas`/`scikit-learn`.

`jupyter` thì khai báo ở root `pyproject.toml` — chỉ dùng để khám phá dữ liệu, không bao giờ cần lúc chạy API.

Lý do tách theo "cần lúc runtime API hay không" thay vì "training vs API": production image build bằng `uv sync --frozen --package app` (xem `template/backend/Dockerfile`) chỉ cài dependency khai báo trong `backend/pyproject.toml` — dependency chỉ khai báo ở root sẽ không có trong image production.
