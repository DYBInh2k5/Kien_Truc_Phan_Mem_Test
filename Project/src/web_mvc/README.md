# README.md
# Final Project: Hệ thống Quản lí Đơn hàng (Order Management System)
Môn học: Software Architecture

## Kiến trúc Hệ thống:
1. **Mô hình lập trình**: n-Tier / Layered Architecture / MVC (Model-View-Controller).
   - `Controllers`: Tầng điều hướng (API Route).
   - `Models`: Tầng thực thể Data (Pydantic / Interface Models).
   - `Services` & `Patterns`: Tầng nghiệp vụ xử lý logic kinh doanh (Business Logic).
   - `Repositories`/`Config`: Tầng truy cập dữ liệu (Data Access).

2. **Chức năng đã đáp ứng**:
   - Login (AuthService).
   - Managing Users (User CRUD trên AuthService).
   - Show "Object-Information" (API hiển thị danh sách tất cả các Đơn Hàng qua Iterator).
   - Search/Find (API Tìm kiếm qua Iterator).

3. **Áp dụng 5 Design Patterns (Phân bổ trong `app/patterns`)**:
   - Creational (CP): **Singleton**, **Factory Method**.
   - Structural (SP): **Facade**.
   - Behavioral (BP): **State**, **Iterator**.

## Hướng dẫn cài đặt & Chạy (Guide/Manual)

1. Đốc Mở terminal ở vị trí thư mục gốc `web_mvc/`.
2. Tạo Virtual Environment và kích hoạt:
   `python -m venv venv`
   `.\venv\Scripts\activate` (Với Windows) / `source venv/bin/activate` (Với Mac/Linux)
3. Cài đặt các thư viện (FastAPI):
   `pip install -r requirements.txt`
4. Khởi động hệ thống:
   `python main.py`
5. Truy cập API Giao diện Đồ Họa (Swagger UI):
   Mở trình duyệt: `http://localhost:8000/docs`. Toàn bộ giao diện Testing nằm trong đó!
