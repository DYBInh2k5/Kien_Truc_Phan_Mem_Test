# 📚 API Documentation - Python FastAPI Microservices

Tài liệu này đóng vai trò như một quyển "Từ điển", mô tả chi tiết các hợp đồng giao tiếp (Contract) giữa các hệ thống Microservices và Endpoint mở ra cho người dùng (Client).

## 1. Giao thức nội bộ: gRPC (Dùng giữa các Services)
Định nghĩa hợp đồng tại file `proto/service.proto`. Order Service sử dụng giao thức này để truy vấn trực tiếp User Service thông qua kết nối TCP siêu tốc (HTTP/2).

### 1.1. Unary RPC Endpoint (1-1)
- **Tên phương thức**: `GetUser`
- **Chức năng**: Fetch chi tiết một Profile User bằng ID truyền vào.
- **Payload Request**:
  ```protobuf
  message UserRequest { int32 user_id = 1; }
  ```
- **Payload Response**: 
  Thành công trả về `UserResponse`, thất bại bắn lỗi `StatusCode.NOT_FOUND` kèm exception gRPC.

### 1.2. Server Streaming RPC (1-N)
- **Tên phương thức**: `StreamUsers`
- **Chức năng**: Mở 1 pipeline liên tục, đẩy từng mảnh dữ liệu của Users qua cho Order Service (thay vì bắt Order Service chờ 1 cục bự).
- **Format**: `stream UserListResponse`

---

## 2. Giao thức ngoại bộ: REST API (Dành cho Client / Frontend)
Được host trên Swagger UI của `Order Service` (Port 8002).

### 2.1. Lấy thông tin Hóa Đơn (`GET /api/orders/{order_id}`)
- **Input**: Đường dẫn path variable chứa `order_id` (Ví dụ `101`).
- **Response Format (JSON 200 OK)**:
  ```json
  {
      "order_id": 101,
      "item": "Laptop Gaming",
      "price": 1500.0,
      "user_info": { "name": "Alice", "email": "alice@example.com" }
  }
  ```
- Ý nghĩa: Backend của API này gọi thầm (under-the-hood) sang User Service bằng phương thức gRPC Unary để bổ sung Object `user_info` vào response.

### 2.2. Nhận stream danh sách User (`GET /api/orders/users/stream`)
- **Input**: None
- **Response**: Trả về `StreamingResponse` kiểu `text/plain`.
- Ý nghĩa: Nhận data dạng Data-chuck, trình duyệt sẽ in ra từng dòng 1 hiển thị theo thời gian thực (giả lập tốc độ load data khổng lồ mà không bị treo trang).

### 2.3. Health Check (`GET /health`)
- Trả về nhịp tim sức khỏe của service, dùng để Docker quyết định xem Container đó có còn "Sống" không để auto-restart.
