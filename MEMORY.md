# MEMORY.md

- Người dùng đang dùng dự án này để học Agile/Scrum — ưu tiên cách phản hồi giúp họ tự tư duy trước khi thấy đáp án, thay vì làm hộ toàn bộ.
- Tài liệu dự án dùng tiếng Việt là ngôn ngữ chính; giữ tên riêng công nghệ nguyên bản (React, FastAPI, XGBoost, API, REST...) khi không có thuật ngữ tương đương tự nhiên.
- Với nội dung có cấu trúc (tài liệu, kế hoạch...), người dùng thường muốn thấy outline trước khi đi vào chi tiết.
- Các thay đổi hiển thị công khai trên GitHub (Issue, Project, Label, Milestone, Pull Request...) nên được xác nhận lặp lại trước mỗi lần thao tác — vì khó hoàn tác và ảnh hưởng đến thứ người khác nhìn thấy.
- Commit message không cần trailer đồng tác giả (Co-Authored-By), viết bằng tiếng Anh, kể cả khi UI/tài liệu miền là ngôn ngữ khác — kiểm tra `git log` trước khi viết commit nếu chưa chắc.
- Repo thuộc tài khoản cá nhân (User), không phải Organization — field "Issue type" dựng sẵn của GitHub không khả dụng ở đây; dùng field `Item Type` (User Story/Task) trong GitHub Project để thay thế.
- GitHub Projects v2 dùng API/scope quyền riêng, tách biệt với quyền truy cập Issues/PR thông thường — đừng giả định token đã có đủ quyền, hãy tự xác minh trước khi thao tác.
- Đặt Status = Done trên GitHub Project sẽ tự động đóng Issue liên kết.
- Tiêu chí chấp nhận của User Story viết bằng văn phong tự nhiên, không thuật ngữ kỹ thuật, kể cả với dữ liệu/mô hình; ưu tiên Given-When-Then hơn Checklist khi cần dễ hình dung kịch bản cho nhiều vai trò đọc.
- Hệ thống auth có sẵn trong template (JWT, superuser, quên mật khẩu...) giữ nguyên, không xoá/viết lại — sẵn sàng dùng khi cần đăng nhập riêng cho nhân viên vận hành sau này.
- Comment đóng DoD/cập nhật trạng thái trên Issue chỉ nêu sự thật khách quan đã hoàn thành (đã test, đã có PR...), và tránh văn phong tự tham chiếu.
- Khi một User Story đã có sẵn sub-issue trên GitHub, viết spec kỹ thuật bằng cách comment lên issue cha và từng sub-issue liên quan — không tạo issue mới hay nhãn mới.
