# 🐳 Docker Deployment & Architecture Guide

Tài liệu này dùng để giải thích cho giảng viên về cách chúng ta sử dụng công nghệ ảo hóa mạng của **Docker** và **Docker Compose** để kết nối microservices. Bạn có thể chép thông tin này vào Slide PPTx.

## 1. Cấu trúc Hình thái (Topology Setup)
Chúng ta có 2 block độc lập hoàn toàn (cả về mã nguồn lẫn biến môi trường):
- **Node A**: User Service (FastAPI + gRPC Server)
- **Node B**: Order Service (FastAPI + gRPC Client)

Nếu không có Docker, 2 hệ thống này muốn nói chuyện được với nhau phải hard-code bằng các IP ảo (localhost) và tự quản lý môi trường Python rất rườm rà.

## 2. Lát cắt Dockerfile
Cả 2 dịch vụ đều được gói trong Alpine/Slim Python image siêu nhẹ (`python:3.10-slim`).
Điểm nổi bật của file `Dockerfile`:
- Nó tự động tải thư viện Protobuf và **biên dịch (compile)** file `service.proto` ra Python Scripts ảo trước khi Server hoạt động. Tức là người Review Code không bao giờ thấy thư viện sinh tự động rác trên Github, nó chỉ tồn tại bên trong Docker.
- Code đảm bảo sạch, tuân thủ Continuous Integration (CI).

## 3. Cấu hình Docker Compose Network
Quan sát file `docker-compose.yml`, chúng ta rút ra các điểm ăn tiền:
1. **Private Network**: Định nghĩa `networks: micro-network`. Hai service nằm gọn trong cái private net này. An toàn tuyệt đối.
2. **DNS Resolution**: Trong code của Order Service, mình không hề trỏ `127.0.0.1` hay `192.168.x.x` để tìm User Service. Mình gọi trực tiếp biến môi trường:
   `USER_SERVICE_URL=user-service:50051`.  
   -> Docker tự động làm **Service Discovery** phân giải cái chữ `user-service` thành IP mạng nôi bộ. Rất linh hoạt và đáp ứng đúng Concept "Decoupled Microservices" mà giảng viên dạy trên lớp. 
3. **Orchestration**: Lệnh `depends_on: - user-service` bắt buộc Docker phải khởi động dịch vụ User lên trước, cắm gRPC server sẵn sàng đi rồi nó mới nhả Order Service lên sau, nhằm tránh việc Order Service bị ném Exception "Connection Refused" ngay phút đầu chạy ứng dụng.
