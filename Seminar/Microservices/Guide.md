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
├── service2_order/           # Gọi gRPC sang service 1 & mở FastAPI REST port 8002
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── service3_gateway/         # Cổng bảo vệ, cấp Token & Proxy chuyển tiếp port 8000
    ├── Dockerfile
    ├── main.py
    └── requirements.txt
```

## Yêu cầu

- Đã cài đặt [Docker](https://www.docker.com/) và Docker Compose trên máy của bạn.

## 🛠️ Hướng dẫn Vận hành Dự án (Chạy và Tắt)

Vì hệ thống được thiết kế theo cấu trúc Microservices gồm nhiều thành phần độc lập, chúng ta sử dụng **Docker Compose** để quản lý, build và chạy đồng thời toàn bộ hệ thống bằng một câu lệnh duy nhất.

### 1. Cách KHỞI ĐỘNG hệ thống (Docker Compose)
Mở cửa sổ **Terminal** hoặc **Command Prompt / PowerShell** trong thư mục dự án `Seminar/Microservices/` và thực hiện:

* **Bước 1: Chạy lệnh build và khởi động ngầm:**
  ```bash
  docker-compose up -d --build
  ```
  *Giải thích ý nghĩa lệnh:*
  * `-d` (Detached mode): Chạy ngầm các container dưới nền, giúp terminal của bạn không bị khóa và có thể tiếp tục gõ lệnh khác.
  * `--build`: Ép buộc Docker biên dịch (compile) lại mã nguồn mới nhất cùng các chú thích code tiếng Việt vừa cập nhật.

* **Bước 2: Kiểm tra xem các Service đã sẵn sàng chưa:**
  * Bạn có thể xem log hoạt động thời gian thực của 3 Service bằng lệnh:
    ```bash
    docker-compose logs -f
    ```
    *(Nhấn `Ctrl + C` để thoát màn hình xem log mà không làm tắt server).*
  * Hoặc gõ lệnh để kiểm tra danh sách container đang chạy:
    ```bash
    docker ps
    ```
    *(Nếu hiện đủ 3 container `python_gateway_service`, `python_user_service`, `python_order_service` là thành công).*

### 2. Cách TẮT hệ thống (Docker Compose)
Sau khi kết thúc buổi thuyết trình hoặc muốn giải phóng tài nguyên CPU/RAM cho máy tính:
1. Mở Terminal tại thư mục `Seminar/Microservices/`.
2. Chạy câu lệnh:
   ```bash
   docker-compose down
   ```
   *Lệnh này sẽ tự động dừng tất cả các container, xóa chúng khỏi bộ nhớ tạm và xóa mạng nội bộ ảo `micro-network` một cách sạch sẽ.*

---

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

### 3. Test trên FastAPI UI của Service 3 (API Gateway - Cổng bảo mật)
Mở trình duyệt: `http://localhost:8000/docs`

- **Bước 1 (Lấy Token):** Chọn API `POST /auth/login`, bấm **Try it out**, điền Username: `admin` và Password: `123456`. Bấm **Execute**. Copy chuỗi token nhận được trong phản hồi JSON.
- **Bước 2 (Xác thực):** Nhấp vào nút **Authorize (hình ổ khóa màu xanh)** ở góc trên bên phải trang Swagger. Dán chuỗi token vừa copy vào ô Value, bấm **Authorize** rồi bấm **Close**.
- **Bước 3 (Truy cập API được bảo vệ):** Mở API `GET /api/orders/{order_id}`, nhập `101` và bấm **Execute**. Gateway sẽ kiểm tra Token hợp lệ, ghi log và Reverse Proxy ngầm chuyển tiếp yêu cầu đến Order Service nội bộ để lấy kết quả.

---

## 🛠️ Phương án chạy dự phòng (Không dùng Docker)

Nếu máy tính trình chiếu của trường gặp lỗi hoặc không cài đặt sẵn Docker Desktop, bạn có thể chạy dự án trực tiếp trên hệ điều hành Windows thông qua script giả lập tự động:

1. Mở cửa sổ **PowerShell** bằng quyền Administrator.
2. Di chuyển đến thư mục dự án và thực thi file chạy local:
   ```powershell
   cd "d:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Seminar\Microservices"
   powershell -ExecutionPolicy Bypass -File .\run_local.ps1
   ```
   *Script sẽ tự động tạo môi trường ảo Python (`venv`), cài đặt thư viện cần thiết, biên dịch file `.proto` và khởi chạy cả 3 cổng dịch vụ lên máy.*

---

## ⚙️ Cấu hình (Config) Chi tiết trong Code

Để dễ dàng theo dõi và chỉnh sửa các tham số của hệ thống, hãy chú ý các tệp và dòng code sau:

1. **Hợp đồng RPC:** Định nghĩa dịch vụ và cấu trúc dữ liệu tại [proto/service.proto](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/proto/service.proto#L24-L30) (Dòng 24 - 30).
2. **Cấu hình Kết nối & Timeout:**
   * URL kết nối gRPC và thời gian timeout của Client được khai báo tại [service2_order/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service2_order/main.py#L22-L23) (Dòng 22 - 23).
   * URL của Order Service chuyển tiếp từ API Gateway được định nghĩa tại [service3_gateway/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service3_gateway/main.py#L15) (Dòng 15).
3. **Mã hóa URL & Port:** Cấu hình mở cổng ra ngoài Internet của các container nằm tại [docker-compose.yml](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/docker-compose.yml) (Cổng Gateway `8000` ở dòng 11, cổng User `8001` ở dòng 27, cổng Order `8002` ở dòng 39).
4. **Mock Database:**
   * Bảng người dùng `USERS` nằm ở [service1_user/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service1_user/main.py#L12-L16) (Dòng 12 - 16).
   * Bảng đơn hàng `ORDERS` nằm ở [service2_order/main.py](file:///d:/HSU/2533Semester%203%282025-2026%29/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Seminar/Microservices/service2_order/main.py#L15-L19) (Dòng 15 - 19).
