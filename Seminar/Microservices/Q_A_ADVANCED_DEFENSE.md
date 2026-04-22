# 🛡️ BỘ CÂU HỎI BẢO VỆ CHUYÊN SÂU (ADVANCED Q&A DEFENSE)

Tài liệu này là "Vũ khí bí mật" dự phòng cho buổi Seminar. Khi Giảng viên muốn thử thách xem bạn thực sự tự code hay đi chép, họ sẽ hỏi những câu xoáy sâu vào "What-if" (Sẽ ra sao nếu...). Hãy bình tĩnh học thuộc các câu trả lời dưới đây!

---

## 🛑 TÌNH HUỐNG 1: HỆ THỐNG SẬP (FAULT TOLERANCE)
**❓ Câu hỏi của Thầy Cô:** *"Sẽ ra sao nếu mạng ảo bị nghẽn, hoặc thằng `User Service` tự nhiên bị sập chết? Lúc đó `Order Service` cứ đứng chờ mãi và treo luôn cả hệ thống à?"*

**💡 Trả lời:**
> "Dạ không thưa thầy/cô. Trong file code `main.py` của con Order Service, nhóm em ĐÃ thiết lập cơ chế **Timeout (Thời gian chờ tối đa)**.
> Cụ thể ở dòng code gRPC: `await stub.GetUser(..., timeout=5.0)`. Nếu quá 5 giây mà mạng rớt hoặc User Service chết không trả lời, gRPC sẽ tự động cắt đứt kết nối và Order Service sẽ báo về màn hình lỗi *'503 Service Unavailable: User Service Offline'* chứ hệ thống tuyệt đối không bị dính vòng lặp chờ vô tận (Infinite Hang) gây sập lây chuyền ạ!"

---

## 🛑 TÌNH HUỐNG 2: SO SÁNH CÔNG NGHỆ (gRPC vs REST)
**❓ Câu hỏi của Thầy Cô:** *"Tại sao em phải cực khổ setup Protobuf và gRPC làm gì? Sao không để 2 Service gọi REST API (JSON) cho lẹ?"*

**💡 Trả lời:**
> "Dạ đúng là REST API thì dễ setup hơn, nhưng trong môi trường Microservices thực tế, khi các Server nội bộ chat với nhau hàng triệu lần mỗi giây, thì REST bộc lộ 2 điểm yếu chí mạng:
> 1. REST gửi data bằng cục chữ JSON rất nặng. Còn gRPC nén data thành số Nhị phân (Binary) siêu nhẹ.
> 2. gRPC chạy trên nền HTTP/2, hỗ trợ truyền dữ liệu ống nước liên tục (Streaming RPC), giải quyết bài toán tốn RAM mà REST không làm được. Nhóm em muốn ứng dụng công nghệ hiệu suất cao nhất thưa thầy/cô!"

---

## 🛑 TÌNH HUỐNG 3: BẢO MẬT HỆ THỐNG & API GATEWAY
**❓ Câu hỏi của Thầy Cô:** *"Tại sao cổng của Microservices em giấu đi hết mà lại đẻ ra cái thằng API Gateway làm gì cho rườm rà?"*

**💡 Trả lời:**
> "Dạ đó là mô hình bảo vệ vòng ngoài (Facade/Proxy) ạ!
> Thay vì vứt trần trụi các Microservices ra môi trường Internet để Hacker dễ dàng tấn công ddos hoặc chọc ngoáy, em khóa chúng nó lại dưới đáy mạng Docker nội bộ. Người dùng chỉ có 1 cánh cửa duy nhất là đi qua `API Gateway (Cổng 8000)`. 
> Tại cánh cửa này, em gắn cơ chế **Authentication (Token JWT)**. Anh phải đăng nhập lấy thẻ Token thì em mới mở đường Proxy cho anh đi tiếp. Ngoài ra Gateway còn đóng vai trò **Ghi Log** theo dõi mọi hành vi truy cập nữa ạ!"

---

## 🛑 TÌNH HUỐNG 4: KHẢ NĂNG MỞ RỘNG (SCALABILITY)
**❓ Câu hỏi của Thầy Cô:** *"Dự án em đang dùng Database giả (Dictionary lưu trên RAM). Giả sử giờ có 1 triệu Đơn hàng thì em nâng cấp hệ thống này thế nào?"*

**💡 Trả lời:**
> "Dạ mô hình Microservices này sinh ra là để dễ dàng mở rộng (Scale).
> Nếu nâng cấp lên Thực Tế, em sẽ thay cái biến Dictionary kia bằng 2 cụm Database tách biệt hoàn toàn: Ví dụ User Service dùng `PostgreSQL` (để bảo toàn cấu trúc dữ liệu), còn Order Service lưu thông tin thanh toán khổng lồ em sẽ dùng `MongoDB` (NoSQL để tốc độ lưu siêu nhanh). 
> Cuối cùng, nếu Order Service bị tắc nghẽn, em chỉ cần gõ lệnh Docker sinh ra thêm 5 cái Container Order Service nữa chạy song song thông qua Load Balancer là gánh được 1 triệu User ạ."

---

## 🛑 TÌNH HUỐNG 5: VẤN ĐỀ ĐỒNG BỘ DỮ LIỆU CHÉO
**❓ Câu hỏi của Thầy Cô:** *"Làm sao em đảm bảo tính nhất quán? Ví dụ User bị xóa bên Service 1, thì mấy cái Order liên quan bên Service 2 tính sao?"*

**💡 Trả lời:**
> "Dạ đây là bài toán kinh điển Saga Pattern trong Microservices.
> Hiện tại vì là Seminar nhỏ nên em chưa setup, nhưng nếu triển khai, em sẽ dùng kĩ thuật **Message Queue (Ví dụ Kafka hoặc RabbitMQ)**. 
> Khi 1 User bị xóa ở Service 1, hệ thống không xóa trực tiếp mà nó sẽ bắn 1 cái tin nhắn 'User A đã chết' vào Hàng đợi (Queue). Thằng Service 2 ngồi nghe thấy tin nhắn đó, lập tức tự động vào kho data của mình để đóng băng toàn bộ Order của User A lại. Nó đảm bảo 2 bên xử lý bất đồng bộ nhưng không bao giờ bị lệch dữ liệu."

---
*(Chỉ cần bạn ngâm cứu 5 câu hỏi tình huống này, đảm bảo thầy cô sẽ gật gù khen bạn có tư duy của một kĩ sư phần mềm thực thụ!)*
