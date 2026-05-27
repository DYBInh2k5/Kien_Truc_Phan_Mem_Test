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
  - Code định nghĩa RPC `GetUser` trong file [proto/service.proto](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/proto/service.proto#L26) (Dòng 26).
  - Code xử lý GetUser của Server tại [service1_user/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service1_user/main.py#L22-L33) (Dòng 22 - 33).
  - Code gọi gRPC Client của Order Service tại [service2_order/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service2_order/main.py#L52-L62) (Dòng 52 - 62).
- **Thoại thuyết trình**:
  > "Để hiện thực giao tiếp, đầu tiên nhóm em sử dụng Unary RPC - phương thức gọi 1-1. Ở file proto/service.proto dòng 26, dịch vụ UserService định nghĩa hàm GetUser. Khi có request, phía Order Service đóng vai trò Client tại service2_order/main.py dòng 57 sẽ gọi await stub.GetUser() để truyền ID sang User Service và ngay lập tức nhận về kết quả là Tên Khách Hàng."

---

## 🛑 Slide 6: Kĩ thuật Streaming RPC (Cho Dữ liệu Lớn)
- **Hình ảnh hiển thị trên Slide**:
  - Code StreamUsers của Server dùng `yield` tại [service1_user/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service1_user/main.py#L36-L39) (Dòng 36 - 39).
  - Code Client đọc Stream liên tục bằng `async for` tại [service2_order/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service2_order/main.py#L95-L96) (Dòng 95 - 96).
- **Thoại thuyết trình**:
  > "Nhưng giả sử cần truyền tải danh sách User cực lớn thì gRPC xử lý ra sao? Khác với HTTP REST bắt đợi load xong toàn bộ rồi trả về một khối JSON nặng nề, gRPC Server Streaming mở một đường ống dẫn liên tục. Tại service1_user/main.py dòng 38, chúng em dùng lệnh yield để bắn từng phần tử User về ngay khi đọc được. Phía Client tại service2_order/main.py dòng 95 sử dụng cấu trúc async for response in stub.StreamUsers() để nhận dữ liệu thời gian thực mà không bị nghẽn RAM."

---

## 🛑 Slide 7: Cơ chế Bảo mật tập trung với API Gateway (Điểm Bonus)
- **Hình ảnh hiển thị trên Slide**:
  - Code Middleware ghi log tại [service3_gateway/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service3_gateway/main.py#L18-L28) (Dòng 18 - 28).
  - Code xác thực verify_token và proxy tại [service3_gateway/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service3_gateway/main.py#L42-L65) (Dòng 42 - 65).
- **Thoại thuyết trình**:
  > "Để đảm bảo an ninh, nhóm em xây dựng thêm API Gateway làm chốt chặn duy nhất hướng ra Internet. Tại file service3_gateway/main.py dòng 18-28, Middleware ghi nhận và đo thời gian xử lý của mọi request. Tiếp đó tại dòng 42, hàm verify_token bắt buộc phải xác thực Token JWT khớp thì mới tiến hành chuyển tiếp Proxy (httpx.get ở dòng 60) yêu cầu vào các Service nội bộ bên dưới."

---

## 🛑 Slide 8: Docker Compose & Cơ chế Chịu Lỗi (Fault Tolerance)
- **Hình ảnh hiển thị trên Slide**:
  - File cấu hình [docker-compose.yml](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/docker-compose.yml#L42) (Dòng 42: USER_SERVICE_URL).
  - Code cấu hình gRPC Timeout tại [service2_order/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service2_order/main.py#L23) (Dòng 23) và lúc truyền vào GetUser (Dòng 57).
- **Thoại thuyết trình**:
  > "Để vận hành mượt mà, chúng em bọc cả 3 Service vào Docker Compose. Tại docker-compose.yml dòng 42, chúng em cấu hình cổng gRPC thông qua tên nhãn user-service:50051 thay vì IP cứng. Ngoài ra, để tránh hiện tượng sập lây chuyền (Cascading Failure), tại service2_order/main.py dòng 23, chúng em định nghĩa cờ GRPC_TIMEOUT = 5 giây để ngắt kết nối lập tức nếu User Service không phản hồi."

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
