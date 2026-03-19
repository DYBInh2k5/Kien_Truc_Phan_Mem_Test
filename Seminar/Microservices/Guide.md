# Hướng dẫn Cài đặt & Chạy Seminar Python FastAPI Microservices

Dự án này ứng dụng Python FastAPI và gRPC, theo cấu trúc Microservices (User Service & Order Service). Cả hai chạy trong một network của Docker và sử dụng `docker-compose`.

## Cấu trúc thư mục

```text
Seminar/Microservices/
├── docker-compose.yml
├── proto/
│   └── service.proto         # Chứa Unary & Streaming RPC definition
├── service1_user/            # Service chia sẻ dữ liệu qua gRPC & mở FastAPI REST port 8001
│   ├── Dockerfile
│   ├── main.py               
│   └── requirements.txt
└── service2_order/           # Gọi gRPC sang service 1 & mở FastAPI REST port 8002
    ├── Dockerfile
    ├── main.py
    └── requirements.txt
```

## Yêu cầu

- Đã cài đặt [Docker](https://www.docker.com/) và Docker Compose trên máy của bạn.

## Các lệnh thực thi (Commands)

Do các Microservices này là độc lập nên ta dùng **Docker Compose** để build chung 1 lần:

**B1. Khởi động các services:**

Mở Terminal / Command Prompt trong thư mục `Seminar/Microservices/` và chạy:
```bash
docker-compose up --build
```
*Lưu ý: Bạn có thể thêm cờ `-d` ở cuối để chạy ngầm (detached mode).*

Lúc này, Docker sẽ nạp các file Proto, tự động sinh code ra file `_pb2.py` và `_pb2_grpc.py`, cài đặt các package trong `requirements.txt` và chạy 2 cổng.

**B2. Kiểm tra log khởi động:**

Đảm bảo logs hiện lên thông báo:
```text
python_user_service    | INFO:root:gRPC Server started on port 50051
python_user_service    | INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
...
python_order_service   | INFO:     Uvicorn running on http://0.0.0.0:8002 (Press CTRL+C to quit)
```

## Cách Test / Sử dụng (Demo gRPC)

Bạn hãy test trực tiếp trên Swagger UI (giao diện API của FastAPI) được cung cấp sẵn bằng cách vào trình duyệt web.

### 1. Test trên FastAPI UI của Service 2 (Order Service)
Mở trình duyệt: `http://localhost:8002/docs`

- **Trường hợp 1 (Test Unary):** Mở API `GET /api/orders/{order_id}`
  - Gõ `order_id = 101` -> Chạy thử -> Order Service nhận id `101` là của `user_id = 1`, nó sẽ gọi `Unary RPC` tới Service 1, Service 1 sẽ hồi đáp. Kết quả trả về gồm tên "Alice".
  - Gõ `order_id = 103` -> Gửi `user_id = 99` không tồn tại -> Service 1 trả lỗi 404 qua gRPC, Service 2 báo "User not found".
- **Trường hợp 2 (Test Stream):** Mở trình duyệt vào link: `http://localhost:8002/api/orders/users/stream`
  - Bạn sẽ thấy text trả về liên tục (trễ 0.5 giây / 1 dòng do hàm giả lập `asyncio.sleep()`) mô phỏng luồng `Server Streaming RPC` do Service 1 bắn sang.

### 2. Test trực tiếp API Service 1 (User Service)
- Mở `http://localhost:8001/api/users/1`
- Đây là API REST thông thường của Service 1. 

## Cấu hình (Config) trong Code
- `proto/service.proto`: Nơi khái quát Unary và Streaming RPC.
- Giao thức mạng Docker: Các Container giao tiếp qua host `user-service:50051` (tên của Container trong docker-compose).
