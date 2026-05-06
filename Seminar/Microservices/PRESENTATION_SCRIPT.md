Link Slide: https://gamma.app/docs/Untitled-qnvon3gjvvbmyio


# 🎤 KỊCH BẢN THUYẾT TRÌNH SEMINAR (Py01. Python FastAPI Microservices)

*Tài liệu này là nội dung (thoại thuyết trình) và gợi ý thiết kế cho từng trang Slide (PPTx). Bạn có thể bám sát sườn này để trình bày tự tin trên bục giảng.*

---

## 🛑 Slide 1: Tiêu đề & Giới thiệu
- **Hình ảnh hiển thị trên Slide**:
  - Tên Đề tài: Phát triển Microservices hiệu suất cao với Python FastAPI, gRPC & API Gateway.
  - **Danh sách thành viên thực hiện:**
    - Võ Duy Bình (Nhóm trưởng) - MSSV 22301500
    - Trần Bá Lợi - MSSV 22300326
    - Hồng Bảo Khang - MSSV 22101347
    - Huỳnh Trung Tính - MSSV 22301490
    - Võ Hoàng Sơn - MSSV 22300242
- **Thoại thuyết trình**:
  > "Kính chào Thầy/Cô và các bạn. Hôm nay, em xin được trình bày chuyên đề Seminar Py01: Ứng dụng Python FastAPI kết hợp gRPC và Docker để xây dựng một kiến trúc Microservices hoàn chỉnh. Hệ thống demo của em xoay quanh mô hình Quản lý Đơn hàng - chia làm 3 mảnh ghép độc lập là: API Gateway, Khối User và Khối Order."

---

## 🛑 Slide 2: Vấn đề của Monolithic & Lý do chọn Microservices
- **Hình ảnh hiển thị trên Slide**:
  - Hình minh họa Cục đá to (Monolithic) vs Nhiều mảnh ghép Lego (Microservices).
- **Thoại thuyết trình**:
  > "Trong các thiết kế trước đây, toàn bộ logic và Database đều nằm trong 1 khối nguyên khối (Monolithic). Nhược điểm là nếu modul giỏ hàng bị sập, toàn bộ web sập theo. Để khắc phục, em đã xé lẻ chức năng thành các Microservices: mỗi Service chạy trên 1 Docker Container riêng và giữ Database riêng."

---

## 🛑 Slide 3: Kiến trúc Hệ Thống Demos
- **Hình ảnh hiển thị trên Slide**:
  - Vẽ hộp chữ nhật 1: `API Gateway` (Port 8000) - Cổng vào duy nhất.
  - Vẽ hộp chữ nhật 2: `User Service` (Port 8001 / Port RPC 50051). Chèn icon database Users.
  - Vẽ hộp chữ nhật 3: `Order Service` (Port 8002). Chèn icon database Orders.
- **Thoại thuyết trình**:
  > "Trên màn hình là kiến trúc 3 lớp mà em đã xây dựng. Mọi yêu cầu từ Client không được gọi bừa bãi mà phải đi qua chốt chặn API Gateway. Sau khi lọt qua cổng này, request mới đi vào Order Service đòi xem hóa đơn. Khi đó, Order Service có thông tin Món Hàng, nhưng nó KHÔNG có thông tin Tên Khách Hàng. Nó bắt buộc phải gọi sang cơ sở dữ liệu của User Service để hỏi. Em chọn gRPC để làm cầu nối tốc độ cao này."

---

## 🛑 Slide 4: Tại sao gRPC mà không phải REST API?
- **Hình ảnh hiển thị trên Slide**: 
  - So sánh tốc độ: REST (JSON) vs gRPC (Hệ nhị phân Protobuf / HTTP2).
- **Thoại thuyết trình**:
  > "Nhiều nhóm sẽ móc 2 cục API REST với nhau, nhưng em dùng gRPC. Bởi vì khi Server gọi Server, giao thức REST truyền tải chuỗi JSON quá cồng kềnh, phân tích cú pháp chậm. gRPC thì nén rác dữ liệu bằng Binary nhị phân siêu nhẹ, giúp độ trễ giảm đi cỡ 10 lần nhờ chạy trên Protocol HTTP/2."

---

## 🛑 Slide 5: Kĩ thuật Unary RPC (1-1)
- **Hình ảnh hiển thị trên Slide**:
  - Chụp màn hình đoạn code `GetUser` trong file `service.proto`.
  - Chụp màn hình code `await stub.GetUser(...)` bên `main.py` của Order.
- **Thoại thuyết trình**:
  > "Để hiện thực nó, đầu tiên là Unary RPC - phương thức gọi 1-1. Order Service đóng vai Client, gõ cửa sang nhà User Service gửi `user_id` và ngay lập tức nhận về kết quả là Tên Khách Hàng."

---

## 🛑 Slide 6: Kĩ thuật Streaming RPC (Cho Dữ liệu Lớn)
- **Hình ảnh hiển thị trên Slide**:
  - Chụp màn hình góc Code `StreamUsers` trả về dạng `yield`.
- **Thoại thuyết trình**:
  > "Nhưng giả sử cần lấy một triệu danh sách User thì gRPC xử lý ra sao? Khác với HTTP REST bắt đợi 1 giây tải xong rồi trả về 1 cục khổng lồ, gRPC Streaming mở một cái ống dẫn liên tục (pipeline). User Service đọc được data nào là xả ngay sang Order Service qua luồng Stream đó. Nhờ thế, bộ nhớ RAM không bao giờ bị nghẽn (OOM)."

---

## 🛑 Slide 7: Cơ chế Bảo mật tập trung với API Gateway (Điểm Bonus)
- **Hình ảnh hiển thị trên Slide**:
  - Chụp code kiểm tra Token (JWT Auth) tại Gateway.
- **Thoại thuyết trình**:
  > "Để đảm bảo an ninh hệ thống, em xây dựng thêm API Gateway ở phía trước. Tất cả các Microservices bên trong sẽ được giấu hoàn toàn khỏi Internet. Người dùng bắt buộc phải xuất trình thẻ Token hợp lệ ở Gateway thì mới được Gateway Ủy quyền (Proxy) truyền lệnh vào trong cho Order Service. Nếu sai Token, Gateway sẽ tự động chặn đứng."

---

## 🛑 Slide 8: Docker Compose & Cơ chế Chịu Lỗi (Fault Tolerance)
- **Hình ảnh hiển thị trên Slide**:
  - Chụp cấu hình `docker-compose.yml` nhắm vào chữ `USER_SERVICE_URL=user-service:50051`
- **Thoại thuyết trình**:
  > "Toàn bộ cụm Gateway, Order và User được bọc gói tinh gọn trong Docker. Điểm hay của Docker Compose là tính năng Service Discovery. Trong Code em không cấu hình Hard Code IP `127.0.0.1`, em gọi đích danh tên nhãn `user-service`. DNS nội bộ của Docker sẽ phân giải nó. Đồng thời em gắn thêm `Timeout=5s` chặn việc Order Service bị treo chết vĩnh viễn nếu kết nối đứt gãy giữa chừng."

---

## 🛑 Slide 9: Live Demo (Trình chiếu)
- **Hành động (KHÔNG DÙNG SLIDE, TRỰC TIẾP LÊN TRÌNH DUYỆT)**:
  - **Bước 1**: Mở `localhost:8000/docs`. Thử đăng nhập lấy JWT Token, sau đó gọi lấy hóa đơn `101`. Chứng minh API Gateway hoạt động và Proxy thành công.
  - **Bước 2**: Mở `localhost:8001/docs`. Thử gọi lấy User trực tiếp bằng REST JSON để thấy đây là Database độc lập.
  - **Bước 3**: Mở `localhost:8002/docs`. Bấm chạy `Unary RPC` cho order 101 và chạy `Streaming RPC` luồng User để thấy chữ nhấp nháy liên tục mô phỏng luồng Data đang chảy.
- **Thoại thuyết trình**:
  > *"Em xin phép trực tiếp vận hành hệ thống trên môi trường Docker để minh họa toàn bộ lý thuyết vừa rồi..."*

---

## 🛑 Slide 10: Lời Cảm Ơn 
- **Hình ảnh hiển thị trên Slide**:
  - QA / Trả lời câu hỏi. Kèm lời cảm ơn chân thành.
- **Thoại thuyết trình**:
  > "Cảm ơn Cô và các bạn đã theo dõi cơ chế giao tiếp gRPC, API Gateway và quy mô thu nhỏ của một hệ thống Microservices Python điển hình. Xin mời các Thầy/Cô đặt câu hỏi ạ."
