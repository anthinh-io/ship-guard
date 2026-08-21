# Lộ trình dự án (Agile)

Dự án được thực hiện theo mô hình Agile, phù hợp quy mô cá nhân: giữ nhịp sprint hàng tuần để ép tiến độ và phát hiện rủi ro sớm, nhưng bỏ các nghi thức cần nhiều người (daily standup meeting, sprint planning poker).

## Cấu trúc công việc

```
Epic (mục tiêu lớn, kéo dài nhiều sprint)
 └── User Story (một lát cắt giá trị, hoàn thành trong một sprint)
      └── Task (việc kỹ thuật cụ thể để hoàn thành story)
```

Việc theo dõi chi tiết (User Story, Task) được quản lý bằng **GitHub Issues** và **GitHub Projects**, không lặp lại trong tập tin này:

- **Epic** → gắn bằng Label, theo quy trình nghiệp vụ (`epic:performance-monitoring`, `epic:order-management`, `epic:risk-prediction`) — mỗi quy trình kéo dài xuyên suốt nhiều sprint
- **Sprint** → trường **Iteration** trong GitHub Project (template "Iterative development"), mỗi vòng lặp dài 1 tuần, tự động sinh sprint kế tiếp
- **User Story** → 1 Issue, đặt tên theo mẫu _"Là..., tôi muốn..., để..."_, có tiêu chí chấp nhận (Acceptance Criteria) được thêm vào Project
- **Trạng thái** → trường **Status** trong Project, xem qua view board lọc theo iteration hiện tại

Xem chi tiết tại [GitHub Issues](https://github.com/anthinh-io/ship-guard/issues) và [GitHub Projects](https://github.com/anthinh-io/ship-guard/projects).

## Định nghĩa hoàn thành (Definition of Done)

Một Issue/Sprint được coi là hoàn thành khi:

- [ ] Code/chức năng chạy được, không lỗi khi thực thi thử
- [ ] Không có rò rỉ dữ liệu (data leakage) đối với các task liên quan đến mô hình học máy
- [ ] Đã commit/tạo Pull Request tương ứng
- [ ] Tự đánh giá lại Sprint Goal (đạt/chưa đạt) và ghi chú điều chỉnh cho sprint sau ngay trong Issue khi kết thúc iteration

## Bảng phân rã công việc theo Sprint

| Sprint | Thời gian | Mục tiêu | Giá trị mang lại |
| --- | --- | --- | --- |
| Sprint 1 | 17/08 – 23/08/2026 | Có nền tảng vận hành thông suốt: xem số liệu thật trên dashboard, tra cứu đơn theo mã, và nhận dự đoán rủi ro trễ khi tạo đơn mới | Nhân viên vận hành có công cụ tra cứu đơn & dự đoán rủi ro đầu tiên, thay vì làm thủ công |
| Sprint 2 | 24/08 – 30/08/2026 | Quản lý xem được KPI tổng quan hiệu suất giao hàng; nhân viên tìm/lọc được danh sách đơn theo nhu cầu | Quản lý có công cụ giám sát hiệu suất; nhân viên xử lý đơn nhanh hơn nhờ lọc danh sách |
| Sprint 3 | 31/08 – 06/08/2026 | Nhân viên biết được nguyên nhân chính gây rủi ro trễ (chuẩn bị hàng hay vận chuyển) khi có dự đoán trễ; quản lý xác định được điểm nghẽn nằm ở khâu nào | Nhân viên chọn đúng biện pháp can thiệp thay vì đoán mò; quản lý có căn cứ điều chỉnh vận hành đúng chỗ |
| Sprint 4 | 07/08 – 13/09/2026 | Quản lý xem được tỷ lệ đánh giá thấp liên quan đến trễ; độ tin cậy của dự đoán rủi ro được cải thiện qua thử nghiệm | Quản lý gắn được hiệu suất vận hành với trải nghiệm khách hàng; nhân viên tin tưởng hơn vào dự đoán khi ra quyết định |
