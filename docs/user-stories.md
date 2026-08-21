# User Stories — Ship Guard

Danh sách User Story đã phân rã từ 3 quy trình nghiệp vụ mô tả trong [Phân tích quy trình nghiệp vụ](business-process-analysis.md), dùng làm tài liệu tham chiếu khi tạo Issue trên GitHub Project (mỗi story tương ứng 1 Issue, gắn Epic label và Item type = User Story).

## Performance Monitoring (`epic:performance-monitoring`)

### 1. Xem tỷ lệ đúng hạn và trễ trên dashboard

Là quản lý hậu cần, tôi muốn xem tỷ lệ đơn giao đúng hạn/trễ trên dashboard, để nắm nhanh hiệu suất giao hàng hiện tại mà không cần tổng hợp thủ công.

**Giá trị mang lại:** Quản lý cần một con số đáng tin cậy về hiệu suất giao hàng, xem được bất cứ lúc nào — thay vì phải dò từng đơn thủ công để có cái nhìn tổng quan.

**Tiêu chí chấp nhận**

Kịch bản: Tính tỷ lệ trên các đơn đã giao xong
- **Given** hệ thống đã có các đơn hàng với ngày giao thực tế
- **When** quản lý mở dashboard
- **Then** hệ thống hiển thị tỷ lệ đúng hạn và tỷ lệ trễ, tính trên đúng những đơn đã giao xong

Kịch bản: Loại trừ đơn chưa giao khỏi tỷ lệ
- **Given** có đơn chưa có ngày giao thực tế (chưa giao xong)
- **When** hệ thống tính tỷ lệ đúng hạn/trễ
- **Then** đơn đó không được tính vào tỷ lệ — tránh làm sai lệch con số vì dữ liệu chưa hoàn chỉnh

Kịch bản: Chưa có dữ liệu nào đủ điều kiện
- **Given** chưa có đơn nào giao xong trong hệ thống
- **When** quản lý mở dashboard
- **Then** dashboard hiển thị "Chưa có đủ dữ liệu để tính tỷ lệ" thay vì hiện 0% hay báo lỗi

### 2. Xem đầy đủ chỉ số hiệu suất giao hàng

Là quản lý hậu cần, tôi muốn xem đầy đủ các chỉ số hiệu suất giao hàng trên dashboard, để đánh giá được bức tranh vận hành toàn diện, không chỉ một con số tỷ lệ.

**Giá trị mang lại:** Quản lý cần một bộ KPI đầy đủ để tự tin ra quyết định, thay vì chỉ một con số đúng hạn/trễ đơn lẻ như hiện tại.

**Tiêu chí chấp nhận**

Kịch bản: Hiển thị bộ KPI đầy đủ
- **Given** có đơn đã giao xong với dữ liệu người bán và vận chuyển đầy đủ
- **When** quản lý mở dashboard
- **Then** hệ thống hiển thị: tỷ lệ đúng hạn, số đơn trễ, thời gian xử lý trung bình của người bán, thời gian vận chuyển trung bình (tách riêng 2 khâu), phân bố theo vùng, xu hướng theo thời gian

Kịch bản: Loại trừ đơn chưa xác định khỏi mọi KPI
- **Given** một đơn chưa có ngày giao thực tế
- **When** hệ thống tính bất kỳ KPI nào ở trên
- **Then** đơn đó bị loại khỏi KPI đó — áp dụng nhất quán quy tắc "chưa xác định"

Kịch bản: Thiếu dữ liệu cho một KPI cụ thể
- **Given** không có đơn nào đủ dữ liệu để tính một KPI cụ thể
- **When** hiển thị KPI đó
- **Then** hệ thống hiển thị "Chưa có đủ dữ liệu" riêng cho KPI đó, không làm hỏng phần còn lại của dashboard

Ghi chú phạm vi: không bao gồm tỷ lệ đánh giá thấp liên quan trễ — thuộc [Xem tác động của giao trễ đến đánh giá khách hàng](#5-xem-tác-động-của-giao-trễ-đến-đánh-giá-khách-hàng).

### 3. Lọc dashboard theo thời gian khu vực và người bán

Là quản lý hậu cần, tôi muốn lọc dashboard theo khoảng thời gian, khu vực và người bán, để phân tích sâu vào đúng phạm vi mình quan tâm.

**Giá trị mang lại:** Bộ KPI đầy đủ chỉ thực sự hữu ích khi quản lý xem được đúng phạm vi mình quan tâm, thay vì luôn phải nhìn số liệu toàn cục.

**Tiêu chí chấp nhận**

Kịch bản: Lọc theo khoảng thời gian
- **Given** quản lý đang xem dashboard với bộ KPI đầy đủ
- **When** chọn một khoảng thời gian cụ thể
- **Then** toàn bộ KPI cập nhật lại, chỉ tính trên đơn nằm trong khoảng đó

Kịch bản: Lọc theo khu vực
- **Given** quản lý chọn một khu vực cụ thể
- **When** áp dụng bộ lọc
- **Then** toàn bộ KPI chỉ tính trên đơn thuộc khu vực đó

Kịch bản: Lọc theo người bán
- **Given** quản lý chọn một người bán cụ thể
- **When** áp dụng bộ lọc
- **Then** toàn bộ KPI chỉ tính trên đơn của người bán đó

Kịch bản: Bộ lọc không có kết quả
- **Given** bộ lọc thu hẹp đến mức không còn đơn nào phù hợp
- **When** áp dụng bộ lọc
- **Then** hệ thống hiển thị "Không có dữ liệu phù hợp với bộ lọc" thay vì 0% gây hiểu nhầm

Phụ thuộc: bộ KPI đầy đủ ở [Xem đầy đủ chỉ số hiệu suất giao hàng](#2-xem-đầy-đủ-chỉ-số-hiệu-suất-giao-hàng).

### 4. So sánh KPI giữa các kỳ

Là quản lý hậu cần, tôi muốn so sánh bộ KPI của kỳ đang xem với kỳ trước hoặc cùng kỳ năm trước, để biết hiệu suất đang cải thiện hay xấu đi thay vì chỉ nhìn một con số tại một thời điểm.

**Giá trị mang lại:** Một con số KPI tại một thời điểm không tự nó nói lên xu hướng — quản lý cần biết đang tốt lên hay xấu đi so với trước để đánh giá đúng tác động của các quyết định điều chỉnh đã đưa ra.

**Tiêu chí chấp nhận**

Kịch bản: So sánh với kỳ trước liền kề
- **Given** quản lý đang xem dashboard đã áp dụng bộ lọc thời gian
- **When** chọn so sánh với "kỳ trước"
- **Then** hệ thống hiển thị thêm KPI của kỳ liền trước (cùng độ dài khoảng thời gian) cạnh KPI hiện tại, kèm mức chênh lệch

Kịch bản: So sánh với cùng kỳ năm trước
- **Given** quản lý đang xem dashboard
- **When** chọn so sánh với "cùng kỳ năm trước"
- **Then** hệ thống hiển thị KPI của cùng khoảng thời gian năm trước, kèm mức chênh lệch

Kịch bản: Kỳ so sánh không đủ dữ liệu
- **Given** kỳ được chọn để so sánh không có đơn nào đủ điều kiện tính KPI
- **When** hiển thị so sánh
- **Then** phần so sánh hiển thị "Chưa có đủ dữ liệu cho kỳ so sánh" thay vì 0% hay lỗi

Phụ thuộc: bộ lọc ở [Lọc dashboard theo thời gian khu vực và người bán](#3-lọc-dashboard-theo-thời-gian-khu-vực-và-người-bán), áp dụng cho toàn bộ KPI ở [Xem đầy đủ chỉ số hiệu suất giao hàng](#2-xem-đầy-đủ-chỉ-số-hiệu-suất-giao-hàng).

### 5. Xem tác động của giao trễ đến đánh giá khách hàng

Là quản lý hậu cần, tôi muốn biết đơn giao trễ ảnh hưởng thế nào đến đánh giá của khách, để thấy rõ hiệu suất vận hành tác động ra sao đến trải nghiệm khách hàng.

**Giá trị mang lại:** Quản lý cần thấy được hiệu suất vận hành nội bộ ảnh hưởng thế nào đến trải nghiệm thực tế của khách hàng, thay vì chỉ nhìn các con số vận hành tách rời khỏi cảm nhận của khách.

**Tiêu chí chấp nhận**

Kịch bản: Có đủ dữ liệu đánh giá
- **Given** có đơn giao trễ và đã được khách đánh giá
- **When** quản lý mở dashboard
- **Then** hệ thống hiển thị tỷ lệ đánh giá thấp (VD ≤2 sao) trong nhóm đơn trễ, đặt cạnh tỷ lệ tương tự của nhóm đơn đúng hạn để so sánh

Kịch bản: Đơn trễ nhưng chưa có đánh giá
- **Given** đơn giao trễ nhưng khách chưa đánh giá
- **When** tính tỷ lệ
- **Then** đơn đó bị loại khỏi mẫu số — cùng logic "chưa xác định"

Kịch bản: Chưa có đơn nào đủ điều kiện
- **Given** chưa có đơn trễ nào từng được khách đánh giá trong hệ thống
- **When** quản lý mở dashboard
- **Then** hệ thống hiển thị "Chưa có đủ dữ liệu" thay vì 0% hay báo lỗi

## Order Management (`epic:order-management`)

### 6. Tra cứu đơn hàng theo mã

Là nhân viên vận hành, tôi muốn tra cứu một đơn hàng theo mã và xem chi tiết, để trả lời nhanh khi cần biết trạng thái của đơn đó.

**Giá trị mang lại:** Nhân viên cần tìm và xem một đơn cụ thể chỉ trong vài giây, thay vì tra thủ công qua dữ liệu thô — vừa tốn thời gian vừa dễ nhầm.

**Tiêu chí chấp nhận**

Kịch bản: Tra cứu thành công
- **Given** mã đơn nhập vào tồn tại trong hệ thống
- **When** nhân viên tra cứu theo mã đó
- **Then** hệ thống hiển thị đầy đủ sản phẩm, người bán, địa chỉ giao, ngày giao dự kiến, ngày giao thực tế (nếu có) và trạng thái đúng hạn/trễ

Kịch bản: Không tìm thấy đơn
- **Given** mã đơn nhập vào không tồn tại
- **When** nhân viên tra cứu
- **Then** hệ thống thông báo rõ ràng không tìm thấy đơn với mã đó, thay vì để màn hình trống

Kịch bản: Đơn chưa giao xong
- **Given** đơn tồn tại nhưng chưa có ngày giao thực tế
- **When** nhân viên xem chi tiết đơn đó
- **Then** trạng thái hiển thị là "Chưa xác định" — không bị gán nhầm thành đúng hạn hay trễ

Kịch bản: Chưa nhập mã
- **Given** ô nhập mã đơn đang trống
- **When** nhân viên bấm tra cứu
- **Then** hệ thống nhắc nhập mã đơn, không thực hiện tra cứu rỗng

### 7. Tìm và lọc danh sách đơn hàng

Là nhân viên vận hành, tôi muốn tìm và lọc danh sách đơn theo điều kiện, để xử lý nhanh một nhóm đơn cụ thể thay vì tra từng mã một.

**Giá trị mang lại:** Nhân viên cần xử lý nhanh một nhóm đơn cùng lúc, thay vì chỉ tra được một đơn mỗi lần theo đúng mã như hiện tại.

**Tiêu chí chấp nhận**

Kịch bản: Tìm kiếm có kết quả
- **Given** nhân viên nhập điều kiện lọc (trạng thái đúng hạn/trễ/chưa xác định, khoảng thời gian đặt hàng...)
- **When** bấm tìm kiếm
- **Then** hệ thống trả về danh sách đơn khớp điều kiện

Kịch bản: Tìm kiếm không có kết quả
- **Given** không có đơn nào khớp điều kiện lọc
- **When** thực hiện tìm kiếm
- **Then** hệ thống hiển thị "Không tìm thấy đơn nào phù hợp"

Kịch bản: Xem chi tiết từ danh sách
- **Given** danh sách kết quả đang hiển thị
- **When** nhân viên chọn một đơn trong danh sách
- **Then** hệ thống mở đúng trang chi tiết đơn đó (tái dùng chi tiết đã có ở [Tra cứu đơn hàng theo mã](#6-tra-cứu-đơn-hàng-theo-mã))

### 8. Xem dự đoán rủi ro trong trang chi tiết đơn

Là nhân viên vận hành, tôi muốn thấy kết quả dự đoán rủi ro ngay khi xem chi tiết một đơn, để không phải nhớ lại hoặc nhập lại dự đoán đã có.

**Giá trị mang lại:** Nhân viên không phải nhớ lại hay nhập lại dự đoán đã có mỗi khi cần xem lại một đơn — kết quả rủi ro luôn đi kèm chi tiết đơn.

**Tiêu chí chấp nhận**

Kịch bản: Đơn đã có dự đoán
- **Given** đơn đã từng được dự đoán rủi ro
- **When** nhân viên mở trang chi tiết đơn đó
- **Then** trang hiển thị thêm: nhãn dự đoán, xác suất, thời điểm dự đoán

Kịch bản: Đơn chưa có dự đoán
- **Given** đơn chưa từng được dự đoán
- **When** nhân viên xem chi tiết
- **Then** phần dự đoán hiển thị "Chưa có dự đoán cho đơn này"

Phụ thuộc: trang chi tiết đơn ở [Tra cứu đơn hàng theo mã](#6-tra-cứu-đơn-hàng-theo-mã)/[Tìm và lọc danh sách đơn hàng](#7-tìm-và-lọc-danh-sách-đơn-hàng), và kết quả dự đoán đã lưu ở [Nhập đơn mới và nhận dự đoán rủi ro](#11-nhập-đơn-mới-và-nhận-dự-đoán-rủi-ro).

Ghi chú phạm vi: sprint gán cho story này chưa chốt — story chỉ phụ thuộc 2 story tra cứu/tìm đơn và story nhập đơn nhận dự đoán ở trên, không phụ thuộc story phân loại nguyên nhân rủi ro, nên có thể xếp sớm hơn nhóm đó nếu cần.

## Risk Prediction (`epic:risk-prediction`)

### 9. Chuẩn bị dữ liệu lịch sử cho dự đoán rủi ro

Là người phát triển, tôi muốn chuẩn bị dữ liệu lịch sử đã được làm sạch và gắn nhãn đúng hạn/trễ, kèm đủ thông tin về vùng giao hàng, hình thức thanh toán và thời điểm đặt hàng, để có nguyên liệu sẵn sàng cho việc xây dựng mô hình dự đoán rủi ro.

**Giá trị mang lại:** Không có dữ liệu sạch và đủ thông tin thì không thể xây dựng được một mô hình dự đoán đáng tin cậy — thiếu bước này, mọi kết quả dự đoán sau đó đều không có gì bảo đảm là đúng.

**Tiêu chí chấp nhận**

Kịch bản: Gắn nhãn đúng hạn/trễ cho đơn đã giao xong
- **Given** có đơn hàng đã có ngày giao thực tế
- **When** dữ liệu lịch sử được xử lý để chuẩn bị cho việc dự đoán
- **Then** đơn đó được gắn nhãn rõ ràng "đúng hạn" hoặc "trễ", dựa trên chênh lệch giữa ngày giao thực tế và ngày giao đã hẹn

Kịch bản: Bỏ qua đơn chưa giao xong
- **Given** có đơn hàng chưa có ngày giao thực tế
- **When** dữ liệu được xử lý
- **Then** đơn đó không được gắn nhãn đúng hạn/trễ — giữ đúng quy tắc "chưa xác định"

Kịch bản: Đủ thông tin để dự đoán
- **Given** dữ liệu đơn hàng đã được xử lý
- **When** kiểm tra lại dữ liệu trước khi dùng để xây dựng mô hình
- **Then** mỗi đơn đều có đủ thông tin về vùng gửi–vùng nhận, hình thức thanh toán, và thời điểm đặt hàng — không còn thiếu dữ liệu ở những cột quan trọng này

Kịch bản: Tách riêng phần dữ liệu để kiểm tra
- **Given** dữ liệu đã được làm sạch và gắn nhãn đầy đủ
- **When** chuẩn bị dữ liệu cho việc xây dựng mô hình
- **Then** dữ liệu được tách thành phần dùng để huấn luyện và phần dùng để kiểm tra riêng biệt, sao cho phần kiểm tra không "nhìn thấy trước" thông tin đã dùng để huấn luyện — tránh đánh giá kết quả sai lệch

### 10. Xây dựng mô hình dự đoán rủi ro giao trễ

Là người phát triển, tôi muốn có một mô hình dự đoán rủi ro giao trễ mà ứng dụng web có thể gửi thông tin đơn hàng tới và nhận lại kết quả, để có một nguồn dự đoán thật thay vì số liệu giả định.

**Giá trị mang lại:** Biến một biểu mẫu nhập liệu thành một công cụ cảnh báo rủi ro thật sự — không có kết quả dự đoán đáng tin, việc nhập thông tin đơn hàng sẽ không trả về được gì có ý nghĩa cho người dùng.

**Tiêu chí chấp nhận**

Kịch bản: Gửi thông tin đơn và nhận kết quả dự đoán
- **Given** mô hình dự đoán đã được xây dựng xong từ dữ liệu lịch sử đã chuẩn bị
- **When** ứng dụng gửi đầy đủ thông tin một đơn hàng (cân nặng, danh mục, hình thức thanh toán, vùng gửi–nhận, thời điểm đặt hàng) đến hệ thống dự đoán
- **Then** hệ thống trả về kết quả đúng hạn/trễ kèm theo xác suất trễ

Kịch bản: Phân loại mức rủi ro theo ngưỡng đã thống nhất
- **Given** hệ thống đã tính được xác suất trễ cho một đơn
- **When** xác suất đó lớn hơn 50%
- **Then** đơn được xếp vào nhóm "rủi ro cao"; ngược lại được xếp vào nhóm "rủi ro thấp" — ngưỡng 50% là mốc khởi điểm, có ghi lại lý do chọn để xem lại sau khi có thêm dữ liệu thực tế

Kịch bản: Đảm bảo mô hình thực sự nhận ra được rủi ro
- **Given** mô hình đã xây dựng xong
- **When** thử dự đoán với một số đơn mẫu đã biết trước kết quả thật
- **Then** mô hình nhận ra được ít nhất một phần các đơn thực sự bị trễ — không rơi vào tình trạng luôn đoán "đúng hạn" cho mọi đơn

Phụ thuộc: dữ liệu đã chuẩn bị ở [Chuẩn bị dữ liệu lịch sử cho dự đoán rủi ro](#9-chuẩn-bị-dữ-liệu-lịch-sử-cho-dự-đoán-rủi-ro).

Ghi chú phạm vi: chưa gồm nhóm nguyên nhân rủi ro (chuẩn bị hàng/vận chuyển) — thuộc [Biết nguyên nhân rủi ro do chuẩn bị hàng hay vận chuyển](#12-biết-nguyên-nhân-rủi-ro-do-chuẩn-bị-hàng-hay-vận-chuyển).

### 11. Nhập đơn mới và nhận dự đoán rủi ro

Là nhân viên vận hành, tôi muốn nhập thông tin đơn mới và nhận ngay dự đoán đúng hạn/trễ kèm xác suất, để biết trước rủi ro và chủ động xử lý thay vì chờ khách phàn nàn.

**Giá trị mang lại:** Biến quy trình xử lý đơn hàng từ phản ứng (khách báo trễ mới biết) sang chủ động (biết trước để can thiệp kịp thời).

**Tiêu chí chấp nhận**

Kịch bản: Rủi ro cao
- **Given** nhân viên đã nhập đầy đủ thông tin đơn (cân nặng, danh mục, hình thức thanh toán, vùng người bán–người mua, thời điểm đặt hàng) và gửi yêu cầu dự đoán
- **When** hệ thống dự đoán trả về xác suất trễ lớn hơn 50%
- **Then** hệ thống gắn nhãn "Rủi ro cao" trên giao diện và lưu lại nhãn, xác suất, thời điểm dự đoán vào đơn, kèm trạng thái xử lý mặc định "Chưa xử lý"

Kịch bản: Rủi ro thấp
- **Given** thông tin đơn đã nhập đầy đủ và hợp lệ, đã gửi yêu cầu dự đoán
- **When** hệ thống dự đoán trả về xác suất trễ từ 50% trở xuống
- **Then** hệ thống gắn nhãn "Rủi ro thấp" và lưu kết quả tương tự

Kịch bản: Thiếu thông tin bắt buộc
- **Given** nhân viên bỏ trống một trường bắt buộc
- **When** nhân viên bấm nhận dự đoán
- **Then** hệ thống báo lỗi ngay tại trường đó và không gửi yêu cầu dự đoán

Phụ thuộc: kết quả từ [Xây dựng mô hình dự đoán rủi ro giao trễ](#10-xây-dựng-mô-hình-dự-đoán-rủi-ro-giao-trễ).

### 12. Biết nguyên nhân rủi ro do chuẩn bị hàng hay vận chuyển

Là nhân viên vận hành, tôi muốn biết rủi ro trễ đến từ khâu chuẩn bị hàng hay khâu vận chuyển, để chọn đúng biện pháp can thiệp thay vì đoán mò.

**Giá trị mang lại:** Phân tách nguyên nhân giúp nhân viên chọn đúng biện pháp can thiệp — tránh đổi đơn vị vận chuyển trong khi lỗi thực chất nằm ở người bán chuẩn bị hàng chậm, hoặc ngược lại.

**Tiêu chí chấp nhận**

Kịch bản: Rủi ro cao — hiển thị nguyên nhân
- **Given** nhân viên nhập thông tin đơn và nhận kết quả rủi ro cao (>50%)
- **When** xem kết quả dự đoán
- **Then** hệ thống hiển thị thêm nhóm nguyên nhân chính: "Rủi ro do chuẩn bị hàng" hoặc "Rủi ro do vận chuyển"

Kịch bản: Rủi ro thấp — không cần nguyên nhân
- **Given** kết quả dự đoán là rủi ro thấp
- **When** xem kết quả
- **Then** hệ thống không hiển thị nhóm nguyên nhân (không cần thiết vì không phải can thiệp)

Ghi chú phạm vi: mở rộng mô hình dự đoán ở [Xây dựng mô hình dự đoán rủi ro giao trễ](#10-xây-dựng-mô-hình-dự-đoán-rủi-ro-giao-trễ) để trả thêm nhóm nguyên nhân.

### 13. Tổng hợp nguyên nhân rủi ro trên các đơn mới

Là quản lý hậu cần, tôi muốn biết trong các đơn mới có nguy cơ trễ, nguyên nhân chủ yếu đang nằm ở khâu nào, để điều chỉnh vận hành đúng chỗ.

**Giá trị mang lại:** Kết nối dữ liệu dự đoán rủi ro với góc nhìn quản lý, giúp xác định điểm nghẽn hiện tại (dựa trên đơn mới) thay vì chỉ nhìn KPI lịch sử đã xảy ra rồi.

**Tiêu chí chấp nhận**

Kịch bản: Có dữ liệu để tổng hợp
- **Given** có các đơn được dự đoán rủi ro cao trong một khoảng thời gian gần đây
- **When** quản lý xem phần tổng hợp nguyên nhân
- **Then** hệ thống hiển thị tỷ lệ: bao nhiêu % do chuẩn bị hàng, bao nhiêu % do vận chuyển

Kịch bản: Chưa có dữ liệu để tổng hợp
- **Given** chưa có đơn nào được dự đoán rủi ro cao trong khoảng thời gian đó
- **When** xem phần tổng hợp
- **Then** hệ thống hiển thị "Chưa có đủ dữ liệu"

Ghi chú phạm vi: dùng dữ liệu từ các dự đoán mới ở [Biết nguyên nhân rủi ro do chuẩn bị hàng hay vận chuyển](#12-biết-nguyên-nhân-rủi-ro-do-chuẩn-bị-hàng-hay-vận-chuyển) — khác nguồn với KPI thời gian xử lý/vận chuyển ở [Xem đầy đủ chỉ số hiệu suất giao hàng](#2-xem-đầy-đủ-chỉ-số-hiệu-suất-giao-hàng), vốn dùng dữ liệu lịch sử đã giao xong.

### 14. Đánh giá độ chính xác của các dự đoán đã đưa ra

Là quản lý hậu cần, tôi muốn xem mức độ chính xác thực tế của các dự đoán rủi ro đã đưa ra trước đó, để biết có nên tin tưởng dùng dự đoán làm căn cứ ra quyết định hay không.

**Giá trị mang lại:** Quản lý cần bằng chứng cụ thể để biết có nên tin dùng dự đoán rủi ro để ra quyết định hay không — một con số xác suất không ai biết đáng tin đến đâu thì vô nghĩa. Đến thời điểm này, các đơn đã dự đoán trước đó có đủ thời gian trôi qua so với thời gian giao trung bình của Olist (~12 ngày) để bắt đầu có kết quả thực tế đối chiếu.

**Tiêu chí chấp nhận**

Kịch bản: Có đơn đủ điều kiện đối chiếu
- **Given** có đơn đã từng được dự đoán rủi ro VÀ nay đã có ngày giao thực tế
- **When** quản lý mở phần "Độ chính xác dự đoán"
- **Then** hệ thống hiển thị tỷ lệ dự đoán đúng — số đơn có nhãn dự đoán khớp kết quả thực tế, trên tổng số đơn đã đối chiếu được

Kịch bản: Đơn chưa đủ điều kiện đối chiếu
- **Given** đơn đã dự đoán nhưng chưa có ngày giao thực tế
- **When** hệ thống tính độ chính xác
- **Then** đơn đó bị loại khỏi phép tính

Kịch bản: Chưa có đơn nào đủ điều kiện
- **Given** chưa có đơn nào đủ điều kiện đối chiếu
- **When** quản lý mở phần này
- **Then** hệ thống hiển thị "Chưa có đủ dữ liệu để đánh giá độ chính xác"

Phụ thuộc: kết quả dự đoán đã lưu ở [Nhập đơn mới và nhận dự đoán rủi ro](#11-nhập-đơn-mới-và-nhận-dự-đoán-rủi-ro).

Ghi chú phạm vi: đây là bước đo lường độ chính xác — chưa bao gồm hành động cải thiện model dựa trên kết quả đo được (nằm ngoài phạm vi 4 sprint hiện tại).
