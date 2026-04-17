# 🎮 KỊCH BẢN THỰC HÀNH DEMO SEMINAR TRÊN LỚP (Live Demo)

Bản hướng dẫn này chỉ đích danh từng cú click chuột, gõ phím để bạn "vừa nói vừa làm" lôi cuốn sự chú ý của mọi người 100% trong buổi thiết trình.

---

## 🧰 BƯỚC 1: KHỞI ĐỘNG HỆ THỐNG (CHUẨN BỊ 5 PHÚT TRƯỚC KHI LÊN BẢNG)
*Chọn 1 trong 2 cách sau tùy theo cấu hình máy tính trình chiếu:*

- **Cách 1 (Ngầu nhất - Dùng Docker)**: 
  - Mở Terminal ở thư mục `Seminar\Microservices`.
  - Gõ: `docker-compose up --build`. Chờ máy ảo nạp xong.
- **Cách 2 (An toàn nhất - Chạy trực tiếp Python)**:
  - Nếu máy trường không có Docker, bạn chỉ cần gõ đúng một chữ: `.\run_local.ps1` vào PowerShell, script sẽ tự động giả lập 2 Microservices trên localhost cho bạn.

*(Giữ màn hình nền đen của Terminal để mọi người thấy log server nhảy chữ cho chuyên nghiệp).*

---

## 🎭 BƯỚC 2: DEMO KẾT NỐI gRPC 1-1 (UNARY RPC)
*Mục đích: Chứng minh hệ thống Order có thể liên lạc xuyên không gian sang hệ thống User.*

1. Trong lúc trình bày trên bục, bạn hãy tự tin bật trình duyệt Web và truy cập màn hình hệ thống tại cống chính: http://localhost:8002/docs.
2. Bạn trỏ chuột bấm vào dòng: **`GET /api/orders/{order_id}`**.
3. Nhấp vào nút màu trắng **Try it out** (Nằm ở góc phải).
4. Bạn gõ số `101` vào cái ô tên là `order_id` vừa hiện ra.
5. Dõng dạc nói: *"Để biểu diễn cho thầy/cô xem, em sẽ tra cứu thử hóa đơn mã 101"*, sau đó bạn nhấn dứt khoát nút **Execute** màu xanh dương bự. 
6. (Đợi 1 giây), bạn kéo con trượt xuống dưới, khoanh vùng vào kết quả: 
```json
{
  "order_id": 101,
  "item": "Laptop Gaming",
  "price": 1500.0,
  "user_info": {
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```
**🗣️ Kịch bản thuyết trình lúc này:** 
> "Cô thấy không ạ? Hệ thống Order của bọn em chỉ giữ giá bán Laptop và ID người mua. Nhưng thông tin Alice@example.com hoàn toàn được bọn em lấy ngầm xuyên băng thông gRPC từ Microservice số 2 trả về theo thời gian thực!"

---

## 🎭 BƯỚC 3: DEMO KẾT NỐI LUỒNG DATA (STREAMING RPC)
*Mục đích: Khẳng định sức mạnh của gRPC so với JSON thông thường ở chỗ tối ưu đường truyền (Streaming).*

1. Quay lại màn hình Swagger UI, bạn đóng khối `GET /api/orders/{order_id}` lại và mở khối **GET /api/orders/users/stream** bên dưới lên.
2. Vẫn nhấp vào **Try it out**.
3. Vẫn nhấn mạnh tay vào nút **Execute**.
4. **THỜI KHẮC KIẾM ĐIỂM Ở CHỖ NÀY!** Bạn hãy chỉ tay vào ô kết quả (Server response), bảng kết quả sẽ KHÔNG load ra một cái eo một lần, mà bạn sẽ thấy dòng chữ:
```text
Received Signal -> User ID: 1, Name: Alice
(Chớp nháy 0.5 giây)
Received Signal -> User ID: 2, Name: Bob
(Chớp nháy 0.5 giây) 
Received Signal -> User ID: 3, Name: Charlie
...
```
**🗣️ Kịch bản thuyết trình lúc này:** 
> "Nếu dùng API thường, nó phải ngâm tải đủ 1 triệu con User vào vòng lặp rồi mới hiển thị một cục, dẫn tới quá tải RAM (Memory OOM) dẫn đến giật Lag app của Client. Bọn em dùng kĩ thuật Pipeline Streaming qua gRPC. Service A xử lý được bao nhiêu dòng thì 'xả' ngay dữ liệu đó về Service B ngay lập tức! Các chớp nháy delay cô thấy lúc nãy mô phỏng hoàn hảo mô hình Real-time Streaming của Microservices đó ạ!"

---

## BƯỚC 4: HẠ MÀN
Sau khi Demo xong, bạn mở Terminal lên bấm phím `Ctrl + C` (hoặc chéo chữ X dẹp luôn cửa sổ) để báo cáo là mình đã hoàn thành trình diễn kết quả Seminar!
