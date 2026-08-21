# Cẩm nang: `karpathy/autoresearch`

## Bối cảnh

Trong lúc làm việc, có đọc qua repo `autoresearch` của Karpathy — một hướng khá thú vị: để AI agent tự sửa code huấn luyện một model GPT nhỏ, chạy thử liên tục qua đêm, giữ lại phiên bản nào tốt hơn. Nghe qua thấy hao hao với việc mình đang làm ở dự án này — cũng là huấn luyện model, cũng đang tìm cách cải thiện chất lượng — nên có lúc suýt nghĩ "hay áp dụng kiểu này luôn". Ghi lại ở đây để sau này không lặp lại nhầm lẫn đó, và cũng để phân biệt rõ hai kiểu tư duy tưởng giống mà khác hẳn nhau.

## Khác biệt về tư duy áp dụng `autoresearch`

Nhìn kỹ thì cái khiến `autoresearch` hoạt động được lại chính là cái mà dự án này không có: một không gian sáng tạo mở, chưa ai biết trước đâu là hướng tốt. Huấn luyện GPT có vô số cách để "sửa" — đổi kiểu attention, đổi cách tính loss, đổi optimizer — mỗi lần sửa là một ý tưởng thật sự mới, và không có công thức nào bảo trước ý tưởng nào sẽ tốt hơn. Agent ở đó có việc để làm vì nó phải viết code cho một ý tưởng chưa từng tồn tại.

Việc huấn luyện XGBoost/Random Forest ở dự án này thì khác hẳn — về bản chất chỉ là gọi một hàm huấn luyện với vài con số tham số. Không có "kiến trúc" nào để sáng tạo lại, không có optimizer tự viết. Nếu có sửa gì, cũng chỉ là dò số trong một khoảng đã biết — việc này một vòng lặp thông thường (hoặc thư viện dò tham số có sẵn) làm tốt hơn, rẻ hơn, không cần AI phải "nghĩ" gì cả.

Lý do quan trọng hơn nữa: dự án đã bỏ khá nhiều công sức chẩn đoán và biết khá rõ chỗ nghẽn nằm ở đâu rồi — không phải ở cách huấn luyện, mà ở chính dữ liệu Olist không chứa đủ thông tin để dự đoán chính xác hơn (không có dữ liệu giao thông thật, tồn kho theo ngày, thời tiết...). Cho dù có để AI tự sáng tạo cách huấn luyện tài tình đến đâu, nó cũng không thể tạo ra thông tin vốn không có trong dữ liệu. `autoresearch` đi tìm kiến trúc tốt hơn vì nó tin (và có cơ sở để tin) rằng kiến trúc là biến số còn chưa tối ưu. Ở dự án này, biến số đó đã được đo và biết rõ giới hạn rồi — tìm thêm theo hướng đó là tìm sai chỗ.

Còn một điểm nữa dễ bỏ sót: nếu cứ thử thật nhiều cấu hình và chọn cấu hình nào cho điểm số tốt nhất trên tập test, trong khi tập test chỉ có khoảng 19 nghìn dòng (và số dòng "trễ" thật sự chỉ khoảng 1.700) — thử càng nhiều, càng dễ vô tình "trúng" một cấu hình ăn may đúng vào đúng tập test đó, chứ không phải nó thật sự tốt hơn. Đây là một cái bẫy thống kê khá tinh vi, dễ tưởng nhầm là cải thiện thật.

Những nguyên tắc *đúng đắn* của `autoresearch` (cách đo lường công bằng) được áp dụng từ trước ở dự án hiện tại:

- Luôn giữ nguyên một bộ chia train/test và một giá trị random seed cố định, để so sánh giữa các lần thử là công bằng.
- Dùng PR-AUC (đo trên toàn bộ đường cong Precision-Recall) thay vì chỉ nhìn F1 ở một ngưỡng cụ thể — tương tự cách `autoresearch` chọn thước đo không phụ thuộc vào những lựa chọn tùy ý (ở đó là vocab size, ở đây là ngưỡng phân loại).

Nói cách khác cái làm cho một thí nghiệm đáng tin không nằm ở việc có AI agent tự viết code hay không, mà nằm ở việc đo lường công bằng và biết rõ mình đang đo cái gì.

## Khái niệm hay bị trộn lẫn

**Dò tham số (hyperparameter tuning) khác với agent tự sửa code.** Dò tham số là thử các con số khác nhau trong một khoảng đã biết trước (ví dụ trọng số lớp từ 1 đến 11) — việc này máy tính làm tốt, không cần AI "hiểu" gì cả. Agent tự sửa code là để AI viết ra một đoạn logic chưa từng có, đòi hỏi khả năng sáng tạo thật sự — chỉ nên dùng khi bài toán thật sự cần sáng tạo, không phải khi chỉ cần thử số.

**"Chưa biết hướng nào tốt" khác với "biết rồi nhưng chưa đạt được".** `autoresearch` phù hợp với vế đầu — không gian chưa khám phá còn rất lớn. Dự án này hiện đang ở vế sau — đã biết rõ giới hạn, vấn đề không phải là chưa tìm ra cách, mà là cách nào cũng sẽ đụng trần giống nhau vì dữ liệu có hạn.

**Deep Learning (mạng nơ-ron, như GPT) khác với Machine Learning cổ điển (như XGBoost, Random Forest).** Hai nhóm này thường bị nhắc chung một hơi vì cùng nằm trong "học máy", nhưng cách huấn luyện, cách tinh chỉnh, và cả tư duy tối ưu khác nhau khá nhiều. Đọc về cách người ta tối ưu một mạng nơ-ron (như `autoresearch`) không tự động áp dụng được cho một mô hình cây quyết định như XGBoost, dù cả hai đều gọi chung là "huấn luyện model".
