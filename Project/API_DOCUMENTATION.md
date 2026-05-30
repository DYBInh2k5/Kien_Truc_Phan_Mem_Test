# TÀI LIỆU KHẢO SÁT & TÀI LIỆU HÓA API (API DOCUMENTATION)
## HỆ THỐNG QUẢN LÝ ĐƠN HÀNG (OMS)

Tài liệu này mô tả chi tiết các điểm cuối API (Endpoints) của hai thành phần: Web API Component (Python FastAPI) và cụm Microservices Component (C# .NET 8.0).

---

## 🖥️ 1. WEB API COMPONENT (Python FastAPI - Cổng 8000)

Tầng Controller tiếp nhận các yêu cầu REST API từ Client Frontend.

### 1.1 Xác thực người dùng (Login)
*   **Endpoint**: `POST /api/auth/login`
*   **Mô tả**: Kiểm tra thông tin tài khoản và cấp token JWT giả lập.
*   **Request Body (JSON)**:
    ```json
    {
      "username": "admin",
      "password": "123"
    }
    ```
*   **Response (Thành công - 200 OK)**:
    ```json
    {
      "message": "Đăng nhập thành công!",
      "token": "fake_jwt_1",
      "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "is_admin": true
      }
    }
    ```
*   **Response (Thất bại - 200 OK)**:
    ```json
    {
      "error": "Tài khoản hoặc mật khẩu không chính xác."
    }
    ```

---

### 1.2 Xem danh sách thành viên (Get Users)
*   **Endpoint**: `GET /api/users`
*   **Mô tả**: Trả về toàn bộ danh sách người dùng được lưu trữ trong SQLite.
*   **Response (200 OK)**:
    ```json
    [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "is_admin": true
      },
      {
        "id": 2,
        "username": "user",
        "email": "user@example.com",
        "is_admin": false
      }
    ]
    ```

---

### 1.3 Đăng ký thành viên mới (Create User)
*   **Endpoint**: `POST /api/users`
*   **Mô tả**: Tạo một tài khoản mới và lưu vào cơ sở dữ liệu SQLite.
*   **Request Body (JSON)**:
    ```json
    {
      "username": "customer1",
      "password": "mysecretpassword",
      "email": "customer1@example.com"
    }
    ```
*   **Response (Thành công - 200 OK)**:
    ```json
    {
      "message": "Đăng ký thành công User ID 3!"
    }
    ```
*   **Response (Thất bại - 200 OK)**:
    ```json
    {
      "error": "Tên tài khoản đã tồn tại!"
    }
    ```

---

### 1.4 Đặt đơn hàng mới (Place Order)
*   **Endpoint**: `POST /api/orders/place`
*   **Mô tả**: Thực thi chu trình đặt hàng phức tạp đi qua Facade Pattern, Factory Method và State Pattern. Sau khi thành công, chèn thông tin đơn hàng vào SQLite.
*   **Request Body (JSON)**:
    ```json
    {
      "product_id": 1,
      "order_type": "express",
      "address": "123 Đường Nguyễn Huệ, Quận 1, TPHCM"
    }
    ```
*   **Response (Thành công - 200 OK)**:
    ```json
    {
      "status": "Success",
      "order_type": "Express",
      "final_state": "Shipped",
      "tracking_code": "Tracking_Code_1716889240",
      "order_id": 103
    }
    ```

---

### 1.5 Tìm kiếm đơn hàng theo ID (Search Order)
*   **Endpoint**: `GET /api/orders/search/{order_id}`
*   **Mô tả**: Tìm kiếm một đơn hàng cụ thể. Sử dụng **Iterator Pattern** để duyệt qua tập hợp `OrderCollection` để tìm ID khớp.
*   **Response (Thành công - 200 OK)**:
    ```json
    {
      "id": 101,
      "details": "Product ID: 1 (Standard) - Address: Quận 3, TPHCM",
      "status": "Shipped",
      "tracking_code": "TRACK_999"
    }
    ```
*   **Response (Thất bại - 200 OK)**:
    ```json
    {
      "error": "Không tìm thấy đơn hàng 999"
    }
    ```

---

### 1.6 Xem tất cả đơn hàng (Get All Orders)
*   **Endpoint**: `GET /api/orders/`
*   **Mô tả**: Trả về toàn bộ danh sách đơn hàng lấy từ SQLite. Sử dụng **Iterator Pattern** để chuyển đổi tập hợp sang dạng danh sách trả về Client.
*   **Response (200 OK)**:
    ```json
    [
      {
        "id": 101,
        "details": "Laptop XYZ",
        "status": "Shipped",
        "tracking_code": "TRACK_999"
      },
      {
        "id": 102,
        "details": "Bàn Phím Cơ",
        "status": "Pending",
        "tracking_code": "TRACK_333"
      }
    ]
    ```

---

## 🔌 2. MICROSERVICES COMPONENT (C# .NET - Cổng 5001, 5002, 5003)

Các dịch vụ API phụ trợ chạy độc lập phục vụ các tác vụ chuyên môn hóa.

### 2.1 SSO Service (Cổng 5001)
*   **API 1**: Đăng nhập qua SSO
    *   **Endpoint**: `POST http://localhost:5001/api/sso/login`
    *   **Request Body**: `{"username": "admin", "password": "123"}`
    *   **Response (200 OK)**:
        ```json
        {
          "message": "SSO Dịch vụ C#: Đăng nhập thành công!",
          "token": "sso_token_secure_admin_xyz",
          "user": { "username": "admin", "email": "admin@sso.csharp" }
        }
        ```
*   **API 2**: Xác thực Token SSO
    *   **Endpoint**: `GET http://localhost:5001/api/sso/verify?token={token}`
    *   **Response (200 OK)**:
        ```json
        {
          "valid": true,
          "user": "admin",
          "source": "SSO C# Microservice"
        }
        ```

---

### 2.2 Search Service (Cổng 5002)
*   **API**: Tìm kiếm đơn hàng nâng cao
    *   **Endpoint**: `GET http://localhost:5002/api/search/orders/{order_id}`
    *   **Response (200 OK)**:
        ```json
        {
          "id": 101,
          "details": "Laptop XYZ (Bản nâng cấp C# Search)",
          "status": "Shipped",
          "tracking_code": "TRACK_999",
          "searched_at": "2026-05-28T16:02:15.1234567+07:00"
        }
        ```

---

### 2.3 Report Service (Cổng 5003)
*   **API**: Thống kê số liệu đơn hàng và doanh số vận chuyển
    *   **Endpoint**: `GET http://localhost:5003/api/report/summary`
    *   **Response (200 OK)**:
        ```json
        {
          "total_orders": 52,
          "total_revenue": 12450.5,
          "shipping_summary": [
            { "type": "Standard", "count": 38, "cost": 95.0 },
            { "type": "Express", "count": 14, "cost": 210.0 }
          ],
          "system": "C# Statistical Report Microservice",
          "generated_at": "2026-05-28T16:02:20.7890123+07:00"
        }
        ```
