# HƯỚNG DẪN SỬA LỖI (TROUBLESHOOTING GUIDE)
## CÁC LỖI THƯỜNG GẶP KHI VẬN HÀNH DỰ ÁN

Tài liệu này tổng hợp các lỗi phổ biến mà bạn, thầy cô hoặc hội đồng chấm thi có thể gặp phải khi khởi chạy Web Component và cụm C# Microservices, kèm theo cách khắc phục nhanh chóng trong vòng 30 giây.

---

## 🛑 1. LỖI CHẠY SCRIPT POWERSHELL (.ps1)
*   **Triệu chứng**: Khi chạy lệnh khởi động C# Microservices `.\run_microservices.ps1`, PowerShell báo lỗi màu đỏ:
    > *"... cannot be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies ..."*
*   **Nguyên nhân**: Hệ thống bảo mật mặc định của Windows PowerShell ngăn chặn việc thực thi các script tải từ ngoài internet về máy.
*   **Cách khắc phục**:
    *   **Cách 1 (Nhanh nhất)**: Chạy script với cờ bypass chính sách bảo mật tạm thời:
        ```powershell
        powershell -ExecutionPolicy Bypass -File .\run_microservices.ps1
        ```
    *   **Cách 2**: Cho phép chạy tất cả các script trên máy cục bộ bằng cách mở PowerShell bằng quyền Administrator và chạy:
        ```powershell
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
        # Chọn Y (Yes) hoặc A (Yes to All) khi được hỏi.
        ```

---

## 🛑 2. LỖI XUNG ĐỘT CỔNG CHẠY (PORT IS ALREADY IN USE)
*   **Triệu chứng**: Khi chạy Web FastAPI báo lỗi `[Errno 98] Address already in use` hoặc C# báo lỗi `Failed to bind to address http://localhost:5001`.
*   **Nguyên nhân**: Cổng 8000, 5001, 5002 hoặc 5003 đang bị chiếm dụng bởi một ứng dụng khác (ví dụ: dự án cũ chưa tắt sạch, hoặc các service khác của Docker đang chạy ngầm).
*   **Cách khắc phục**:
    *   **Bước 1: Tìm ID của tiến trình đang chiếm cổng** (Ví dụ cổng 8000):
        *   *Trên Windows (PowerShell)*:
            ```powershell
            netstat -ano | findstr :8000
            ```
            *(Bạn sẽ thấy một dòng kết thúc bằng một con số ở cuối, ví dụ: `14256` - đó là Process ID (PID)).*
    *   **Bước 2: Tắt tiến trình đó**:
        *   *Trên Windows (PowerShell)*:
            ```powershell
            taskkill /F /PID 14256
            ```
            *(Thay thế `14256` bằng PID thật vừa tìm thấy).*

---

## 🛑 3. LỖI DOCKER TRÊN MÁY WINDOWS
*   **Triệu chứng**: Chạy `docker-compose up` báo lỗi:
    > *"docker: Cannot connect to the Docker daemon. Is the docker daemon running?"*
*   **Nguyên nhân**: Ứng dụng **Docker Desktop** chưa được mở hoặc dịch vụ Docker daemon đang bị treo.
*   **Cách khắc phục**:
    1.  Mở Docker Desktop trên máy tính của bạn.
    2.  Chờ 1-2 phút cho biểu tượng chú cá voi ở góc dưới bên trái chuyển sang màu **Xanh lá (Engine Running)**.
    3.  Thử chạy lại câu lệnh `docker-compose up -d --build`.

---

## 🛑 4. LỖI DATABASE SQLITE BỊ KHÓA (DATABASE IS LOCKED)
*   **Triệu chứng**: Giao diện báo lỗi `sqlite3.OperationalError: database is locked` khi cố gắng thực hiện đặt hàng hoặc thêm User mới.
*   **Nguyên nhân**: Có một ứng dụng khác (như phần mềm xem database DB Browser for SQLite) đang mở tệp `orders.db` ở chế độ chỉnh sửa (Write Mode) và chưa lưu/đóng kết nối, làm SQLite khóa tệp lại.
*   **Cách khắc phục**:
    1.  Đóng các công cụ quản lý cơ sở dữ liệu bên ngoài đang kết nối tới tệp `orders.db`.
    2.  Nếu vẫn bị khóa, tắt server FastAPI và bật lại để giải phóng hoàn toàn kết nối bị treo.

---

## 🛑 5. LỖI THIẾU .NET SDK KHI CHẠY DỰ ÁN C#
*   **Triệu chứng**: Khi chạy lệnh `dotnet run`, hệ thống báo lỗi không nhận dạng được lệnh hoặc báo thiếu SDK:
    > *"The command 'dotnet' could not be found..."* hoặc yêu cầu cài đặt .NET Core.
*   **Nguyên nhân**: Máy tính chưa cài đặt .NET SDK hoặc biến môi trường PATH chưa nhận diện.
*   **Cách khắc phục**:
    1.  Tải và cài đặt bản **.NET SDK 8.0** hoặc **.NET SDK 9.0** chính thức từ trang chủ Microsoft.
    2.  Khởi động lại cửa sổ PowerShell/CMD để hệ thống cập nhật lại các biến môi trường mới nhất.
