# 🎮 KỊCH BẢN THỰC HÀNH DEMO SEMINAR TRÊN LỚP (Live Demo Toàn Diện)

Bản hướng dẫn này chỉ đích danh từng cú click chuột, gõ phím để bạn "vừa nói vừa làm" lôi cuốn sự chú ý của mọi người 100% trong buổi thiết trình. Nó bao trọn cấu trúc 3 Microservices gồm: **API Gateway**, **User Service** và **Order Service**.

---

## 🧰 BƯỚC 1: KHỞI ĐỘNG HỆ THỐNG
*Chọn 1 trong 2 cách sau tùy theo cấu hình máy tính trình chiếu:*

- **Cách 1 (Ngầu nhất - Dùng Docker)**: 
  - Đảm bảo Docker Desktop đang bật.
  - Mở Terminal ở thư mục `Seminar\Microservices`.
  - Gõ: `docker-compose up -d`. Chờ máy ảo nạp xong.
- **Cách 2 (An toàn nhất - Chạy trực tiếp Windows PowerShell)**:
  - Nếu máy trường lỗi Docker, bạn gõ lệnh: `powershell -ExecutionPolicy Bypass -File .\run_local.ps1` vào PowerShell, script sẽ tự động giả lập trọn vẹn cụm Microservices trên máy bạn.

*(Giữ màn hình nền đen của Terminal để mọi người thấy log server nhảy chữ cho chuyên nghiệp).*

---

## 🛡️ BƯỚC 2: DEMO CỔNG CHÍNH API GATEWAY (PORT 8000)
*Mục đích: Biểu diễn cơ chế bảo mật tập trung (Authentication & Proxy).*

1. Mở trình duyệt truy cập: `http://localhost:8000/docs`.
2. **🗣️ Thuyết trình:** *"Thưa thầy cô, đây là API Gateway. Nó đóng vai trò là Cổng gác duy nhất để người ngoài giao tiếp với hệ thống mạng nội bộ. Mọi truy cập đều bị khóa nếu không có thẻ Token."*
3. Bạn click vào biểu tượng **ổ khóa (Authorize)** nằm góc trên bên phải.
4. Nhập Username: `admin` và Password: `123456`. Sau đó click **Authorize** rồi bấm Close.
5. Cuộn xuống khối **`GET /api/orders/{order_id}`**, bấm **Try it out**, nhập số `101` và nhấn **Execute**.
6. **🗣️ Thuyết trình:** *"Ngay khi Gateway nhận thấy Token hợp lệ, nó lập tức Proxy (Chuyển tiếp ngầm) yêu cầu này thẳng xuống hệ thống Order Service đang giấu kín trong bóng tối để xử lý."*

---

## 👤 BƯỚC 3: DEMO USER SERVICE ĐỘC LẬP (PORT 8001)
*Mục đích: Chứng minh Service được bóc tách dữ liệu độc lập.*

1. Mở một Tab trình duyệt mới, truy cập: `http://localhost:8001/docs`.
2. Mở khối **`GET /api/users/{user_id}`**, bấm **Try it out**, nhập số `2`.
3. Nhấn **Execute**.
4. **🗣️ Thuyết trình:** *"Đây là Microservice quản lý thông tin khách hàng. Nó được lập trình chạy trên một server riêng, database riêng, và có thể truy xuất độc lập hoàn toàn mà không sợ ảnh hưởng hay chia sẻ giật lag với các Service khác trong hệ thống."*

---

## ⚡ BƯỚC 4: DEMO gRPC TỐC ĐỘ CAO (PORT 8002) - TÂM ĐIỂM BÀI NÓI
*Mục đích: Trình diễn sự liên lạc xuyên không gian giữa các Microservice bằng gRPC Unary và Streaming.*

1. Mở Tab thứ ba truy cập cổng: `http://localhost:8002/docs`.
2. Bạn trỏ chuột bấm vào dòng: **`GET /api/orders/{order_id}`**, chọn **Try it out**, nhập `101` rồi bấm **Execute**.
3. **🗣️ Thuyết trình:** *"Hệ thống Order của bọn em chỉ giữ đúng ID của khách. Nhưng cái tên 'Alice' kia là do Order Service gọi điện trực tiếp qua mạng gRPC ngầm (Unary RPC) sang User Service để fetch về thời gian thực!"*

4. Tiếp theo, đóng khối đó lại và mở khối **`GET /api/orders/users/stream`** bên dưới.
5. Vẫn bấm **Try it out**, và nhấn **Execute**.
6. **THỜI KHẮC KIẾM ĐIỂM Ở CHỖ NÀY!** Hãy chỉ tay vào ô kết quả (Server response), dữ liệu sẽ KHÔNG load ra một lần mà chớp nháy từng dòng chữ:
```text
Received Signal -> User ID: 1, Name: Alice
(Chớp nháy)
Received Signal -> User ID: 2, Name: Bob
(Chớp nháy) 
```
7. **🗣️ Thuyết trình dõng dạc:** *"Nếu dùng API thường để tải 1 triệu User, RAM sẽ quá tải (OOM) và app Client sẽ bị treo. Bọn em giải quyết bằng gRPC Streaming. Service A xử lý được bao nhiêu dòng thì 'xả' ngay dữ liệu đó như vòi nước về Service B! Các chớp nháy delay cô thấy lúc nãy mô phỏng hoàn hảo mô hình Real-time Streaming của hệ thống lớn đó ạ!"*

---

## BƯỚC 5: HẠ MÀN
Sau khi Demo xong, bạn mở Terminal lên bấm phím `Ctrl + C` (hoặc chéo chữ X dẹp luôn cửa sổ) để báo cáo là mình đã hoàn thành trình diễn kết quả Seminar!
