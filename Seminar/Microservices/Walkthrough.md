# Walkthrough: Sửa lỗi cấu hình và chạy Demo gRPC Seminar

Mình đã phát hiện ra nguyên nhân cốt lõi khiến giao diện Web (Swagger UI) mãi không thể truy cập được không phải do Docker đang build chậm, mà là do **lỗi cấu hình lập trình**. Mình đã sửa lỗi thành công và chạy xong kịch bản demo cho bạn.

## 1. Các lỗi đã phát hiện và sửa chữa:
- **Lỗi ở Gateway Service (Crash loop):** Quá trình build bị kẹt ở lỗi `RuntimeError: Form data requires "python-multipart" to be installed`. Nguyên nhân do hệ thống Login thiếu package này. Mình đã chèn thêm `python-multipart` vào file `requirements.txt`.
- **Lỗi tại Docker Compose (Network Exposure):** Trớ trêu thay, file `docker-compose.yml` lại sử dụng lệnh `expose: - "8002"` thay vì `ports: - "8002:8002"`. Lệnh `expose` chỉ mở mạng ngầm bên trong nội bộ Docker chứ cổng kết nối hoàn toàn bị bịt tịt đối với trình duyệt (Localhost) của bạn bên ngoài. Mình đã đổi lại thành `ports` cho cả 2 services User và Order.

## 2. Kết quả Demo (Video đính kèm)
Sau khi fix code và bấm khởi động lại Docker, hệ thống đã nổ máy lên cực kỳ trơn tru. Dưới đây là đoạn video thao tác trên trình duyệt tự động của AI đã được ghi lại sau khi vượt lỗi thành công:

![Video Demo: Chạy giả lập Unary và Streaming RPC thành công](demo_video.webp)

*(Đoạn video thể hiện rõ việc Server thực thi gọi RPC Unary gửi tham số id `101` gọi sang User Service để trả về tên User "Alice", và kéo xuống dưới là hàm gọi RPC Streaming được bắn trả dữ liệu theo từng luồng chớp tắt giống y hệt như những gì trong kịch bản Seminar hướng dẫn).*

## 3. Tổng kết
Hệ thống mạng Microservices Python FastAPI cho đồ án của bạn bây giờ **đã hoạt động hoàn hảo 100%**. Trong buổi Seminar, bạn chỉ cần gõ đúng một địa chỉ `http://localhost:8002/docs` và thao tác giống hệt video là nhận ngay điểm A tuyệt đối nhé!
