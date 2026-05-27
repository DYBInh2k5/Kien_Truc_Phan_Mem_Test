# 🛡️ BỘ CÂU HỎI BẢO VỆ CHUYÊN SÂU (ADVANCED Q&A DEFENSE)

Tài liệu này là "Vũ khí bí mật" dự phòng cho buổi Seminar. Khi Giảng viên muốn thử thách xem bạn thực sự tự code hay đi chép, họ sẽ hỏi những câu xoáy sâu vào "What-if" (Sẽ ra sao nếu...). Hãy bình tĩnh học thuộc các câu trả lời dưới đây!

---

## 🛑 TÌNH HUỐNG 1: HỆ THỐNG SẬP (FAULT TOLERANCE)
**❓ Câu hỏi của Thầy Cô:** *"Sẽ ra sao nếu mạng ảo bị nghẽn, hoặc thằng `User Service` tự nhiên bị sập chết? Lúc đó `Order Service` cứ đứng chờ mãi và treo luôn cả hệ thống à?"*

**💡 Trả lời:**
> "Dạ không thưa thầy/cô. Trong file code [service2_order/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service2_order/main.py#L57) dòng 57, nhóm em đã thiết lập cơ chế **Timeout (Thời gian chờ tối đa)**.
> Cụ thể ở dòng 57: `response = await stub.GetUser(request, timeout=GRPC_TIMEOUT)`, và tham số `GRPC_TIMEOUT = 5` được định nghĩa ở dòng 23. Nếu quá 5 giây mà mạng rớt hoặc User Service chết không trả lời, gRPC Client sẽ tự động ném ra ngoại lệ `grpc.aio.AioRpcError` (bắt lỗi ở dòng 65). Order Service sẽ bắt lỗi này và gán thông tin user là `'Service timeout'` chứ hệ thống tuyệt đối không bị treo vĩnh viễn gây sập lây chuyền ạ!"

---

## 🛑 TÌNH HUỐNG 2: SO SÁNH CÔNG NGHỆ (gRPC vs REST)
**❓ Câu hỏi của Thầy Cô:** *"Tại sao em phải cực khổ setup Protobuf và gRPC làm gì? Sao không để 2 Service gọi REST API (JSON) cho lẹ?"*

**💡 Trả lời:**
> "Dạ đúng là REST API thì dễ setup hơn, nhưng trong môi trường Microservices thực tế, khi các Server nội bộ giao tiếp với nhau liên tục, REST bộc lộ nhược điểm là payload JSON rất cồng kềnh.
> Nhóm em dùng gRPC bằng cách định nghĩa hợp đồng trong file [proto/service.proto](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/proto/service.proto#L24-L30) (Dòng 24 - 30). Khi biên dịch, gRPC sẽ mã hóa dữ liệu thành các gói tin **Nhị phân (Binary)** siêu nhẹ và truyền tải qua giao thức `HTTP/2` tiên tiến. Điều này giúp giảm độ trễ truyền dữ liệu nội bộ giữa User Service và Order Service lên tới 7-10 lần so với việc dùng REST API thông thường."

---

## 🛑 TÌNH HUỐNG 3: BẢO MẬT HỆ THỐNG & API GATEWAY
**❓ Câu hỏi của Thầy Cô:** *"Tại sao cổng của Microservices em giấu đi hết mà lại đẻ ra cái thằng API Gateway làm gì cho rườm rà?"*

**💡 Trả lời:**
> "Dạ đó là để áp dụng mẫu thiết kế bảo vệ tập trung (Facade/Reverse Proxy Gateway) ạ!
> Các Microservices bên trong sẽ được cô lập hoàn toàn dưới mạng nội bộ Docker. Người dùng chỉ giao tiếp qua cổng `8000` của API Gateway. Tại file [service3_gateway/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service3_gateway/main.py#L42-L46) dòng 42 - 46, chúng em dùng hàm `verify_token` để kiểm tra Token JWT. Nếu Token không đúng hoặc không có, Gateway sẽ chặn đứng ngay tại cửa ngõ. Chỉ khi có Token hợp lệ, Gateway mới tiến hành gọi `httpx.get` (ở dòng 60) để chuyển tiếp yêu cầu đến các Service bên dưới."

---

## 🛑 TÌNH HUỐNG 4: KHẢ NĂNG MỞ RỘNG (SCALABILITY)
**❓ Câu hỏi của Thầy Cô:** *"Dự án em đang dùng Database giả (Dictionary lưu trên RAM). Giả sử giờ có 1 triệu Đơn hàng thì em nâng cấp hệ thống này thế nào?"*

**💡 Trả lời:**
> "Dạ hiện tại do mô hình Seminar nhỏ nên nhóm em dùng mock dữ liệu dạng biến Dictionary `USERS` tại [service1_user/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service1_user/main.py#L12) dòng 12 và `ORDERS` tại [service2_order/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service2_order/main.py#L15) dòng 15.
> Nếu nâng cấp lên thực tế, nhóm em sẽ thiết lập cơ sở dữ liệu riêng cho từng dịch vụ để đảm bảo nguyên lý **Data Isolation** (Ví dụ: dùng `PostgreSQL` lưu thông tin User tại Service 1 và `MongoDB` lưu trữ các Document Đơn Hàng lớn tại Service 2). Khi cần tải cao, chúng em chỉ cần viết lệnh Docker để nhân bản nhiều instance của Service chạy phía sau một Load Balancer là hệ thống có thể gánh hàng triệu yêu cầu đồng thời."

---

## 🛑 TÌNH HUỐNG 5: VẤN ĐỀ ĐỒNG BỘ DỮ LIỆU CHÉO
**❓ Câu hỏi của Thầy Cô:** *"Làm sao em đảm bảo tính nhất quán? Ví dụ User bị xóa bên Service 1, thì mấy cái Order liên quan bên Service 2 tính sao?"*

**💡 Trả lời:**
> "Dạ đây là bài toán kinh điển Saga Pattern trong Microservices.
> Hiện tại vì là Seminar nhỏ nên em chưa setup, nhưng nếu triển khai, em sẽ dùng kĩ thuật **Message Queue (Ví dụ Kafka hoặc RabbitMQ)**. 
> Khi 1 User bị xóa ở Service 1, hệ thống không xóa trực tiếp mà nó sẽ bắn 1 cái tin nhắn 'User A đã chết' vào Hàng đợi (Queue). Thằng Service 2 ngồi nghe thấy tin nhắn đó, lập tức tự động vào kho data của mình để đóng băng toàn bộ Order của User A lại. Nó đảm bảo 2 bên xử lý bất đồng bộ nhưng không bao giờ bị lệch dữ liệu."

---
*(Chỉ cần bạn ngâm cứu 5 câu hỏi tình huống này, đảm bảo thầy cô sẽ gật gù khen bạn có tư duy của một kĩ sư phần mềm thực thụ!)*
