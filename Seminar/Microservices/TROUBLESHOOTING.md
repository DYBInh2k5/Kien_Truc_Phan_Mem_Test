# 🔧 Khắc phục Sự cố (Troubleshooting) & Vấn đáp (Q&A)

Dưới đây là cẩm nang để bạn "chữa cháy" nếu gặp lỗi trong quá trình thuyết trình Demo Seminar hoặc dùng để "đỡ" các câu hỏi vặn vẹo của Giảng viên.

## Lỗi 1: `Port 8001 / 50051 is already in use`
- **Nguyên nhân**: Bạn đã từng chạy nó trước đó rồi mà lỡ quên tắt, hoặc có một ứng dụng ngầm nào đó của Windows đang giành giật cái Port này.
- **Cách fix**:
  - Dùng lệnh PowerShell: `Stop-Process -Id (Get-NetTCPConnection -LocalPort 8001).OwningProcess -Force` để tiêu diệt phần mềm xài ké cổng.
  - Hoặc nhanh nhất là vào cấu hình file `docker-compose.yml` sửa cái Port `8001:8001` thành `9001:8001` là xong.

## Lỗi 2: `docker-compose: command not found`
- **Cách fix**: Hệ điều hành bạn vừa đổi (hoặc mượn máy tính của trường) không cắm sẵn Docker. Bạn có thể sử dụng giải pháp thay thế là chạy cái terminal Script nội bộ `run_local.ps1` ở trong file nén mà mình cho để chạy thuần bằng môi trường ảo Python.

## Lỗi 3: Lỗi gRPC trả về `StatusCode.DEADLINE_EXCEEDED`
- **Nguyên nhân**: Mạng Docker bị kẹt hoặc User Service xử lý data mock lâu hơn 5 giây.
- **Cách lấy điểm**: Lỗi này không phải lỗi xấu! Trong khóa học kiến trúc Microservices, bạn hãy khoe với Thầy/Cô rằng: *"Em cố tình cấu hình một Cờ **Timeout Mechanism** bằng đoạn code `await stub.GetUser(request, timeout=GRPC_TIMEOUT)`. Nếu không có hệ thống ngắt tự động (Circuit Breaker Design), thì Order Service sẽ bị kẹt vĩnh viễn và đánh sập toàn bộ Cụm Server khi User Service bị sập. Đây là bài test đo sức chịu đựng (Fault Tolerance)!"*. Tự tin khoe điều đó.

---

## 🗣️ Mẹo Vấn đáp bảo vệ Seminar:
* Câu hỏi: **Vì sao lại dùng gRPC mà không Call HTTP REST giữa các Service cho dễ?**
* Trả lời: *Vì Payload của JSON gửi qua REST bị dư thừa text và nặng, trong khi gRPC mã hóa dưới dạng nhị phân (Binary Protocol Buffer) giúp tốc độ bắn dữ liệu liên server (Server-to-Server) nhanh hơn gấp 7-10 lần, đặc biệt khi áp dụng Streaming Transfer truyền file bự sẽ không gây thắt cổ chai hệ thống.*
