# HƯỚNG DẪN VẬN HÀNH DỰ ÁN CUỐI KỲ (RUN GUIDE)
**Hệ thống Quản lý Đơn hàng - Software Architecture Project**

Tài liệu này hướng dẫn chi tiết cách cài đặt môi trường, cấu hình và khởi chạy đồng thời hai thành phần cốt lõi của dự án bài tập lớn:
1.  **Web Component**: Python FastAPI + Giao diện Frontend HTML/CSS/JS + SQLite.
2.  **Microservices Component**: Cụm 3 dịch vụ API viết bằng C# .NET 8.0.

---

## 🛠️ 1. Yêu Cầu Cài Đặt Môi Trường

Trước khi khởi chạy dự án, hãy đảm bảo máy tính của bạn đã cài đặt các công cụ sau:
*   [Python 3.10+](https://www.python.org/downloads/) (Dành cho cụm Web FastAPI)
*   [.NET SDK 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0) (Dành cho cụm Microservices C#)
*   **PowerShell** hoặc **Command Prompt** chạy bằng quyền Administrator trên Windows.

---

## 🖥️ 2. Hướng Dẫn Chạy Web Component (Python FastAPI + Giao Diện Frontend)

Thành phần này chứa toàn bộ logic Web MVC, Design Patterns và cơ sở dữ liệu SQLite thật.

### Bước 1: Mở PowerShell và di chuyển vào thư mục dự án Web
Chạy lệnh di chuyển thư mục (đã bọc ngoặc kép tránh lỗi khoảng trắng đường dẫn):
```powershell
cd "D:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Project\src\web_mvc"
```

### Bước 2: Tạo môi trường ảo Python (Virtual Environment)
```powershell
python -m venv venv
```

### Bước 3: Kích hoạt môi trường ảo
*   **Trên Windows (PowerShell)**:
    ```powershell
    .\venv\Scripts\activate
    ```
*   **Trên Windows (Command Prompt)**:
    ```cmd
    .\venv\Scripts\activate.bat
    ```
*   **Trên macOS/Linux**:
    ```bash
    source venv/bin/activate
    ```

### Bước 4: Cài đặt các thư viện cần thiết
```powershell
pip install -r requirements.txt
```

### Bước 5: Khởi chạy máy chủ API
```powershell
python main.py
```
*Hệ thống sẽ tự động tạo tệp cơ sở dữ liệu SQLite `orders.db` trong thư mục gốc của dự án và nạp dữ liệu mẫu.*

### Bước 6: Sử dụng và Trải nghiệm giao diện
*   **Giao diện người dùng (Frontend - View)**: Mở trình duyệt web truy cập địa chỉ: `http://localhost:8000`
*   **Tài liệu API Swagger**: Mở địa chỉ: `http://localhost:8000/docs`

---

## 🔌 3. Hướng Dẫn Chạy Cụm C# Microservices (.NET 8.0)

Thành phần này chứa 3 Microservices độc lập (SSO, Search, Report) chạy trên 3 cổng khác nhau: 5001, 5002, 5003.

### Cách chạy nhanh bằng Script tự động (PowerShell)

Chúng tôi đã chuẩn bị sẵn một script giúp bạn tự động mở 3 cửa sổ Console riêng biệt tương ứng với 3 Microservices để dễ dàng quan sát log hoạt động thời gian thực.

1.  Mở một cửa sổ PowerShell mới.
2.  Di chuyển tới thư mục chứa microservices:
    ```powershell
    cd "D:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Project\src\microservices_csharp"
    ```
3.  Kích hoạt script khởi động:
    ```powershell
    powershell -ExecutionPolicy Bypass -File .\run_microservices.ps1
    ```
4.  **Kết quả**: Hệ thống sẽ tự động bật thêm 3 cửa sổ CMD chạy các dịch vụ trên các cổng:
    *   **SSOService**: `http://localhost:5001`
    *   **SearchService**: `http://localhost:5002`
    *   **ReportService**: `http://localhost:5003`

### Cách kiểm tra (Test) các cổng Microservices C#
Bạn có thể mở trình duyệt hoặc sử dụng các công cụ như Postman để gọi thử các API này:

*   **Test SSO Service**: Truy cập: `http://localhost:5001/api/sso/verify?token=sso_token_secure_admin_xyz`
    *(Trả về thông tin User Admin được xác thực từ SSO C#)*
*   **Test Search Service**: Truy cập: `http://localhost:5002/api/search/orders/101`
    *(Trả về thông tin đơn hàng 101 được truy vấn từ Microservice Search)*
*   **Test Report Service**: Truy cập: `http://localhost:5003/api/report/summary`
    *(Trả về báo cáo thống kê doanh thu và chi phí vận chuyển)*

---

## 🛑 4. Hướng Dẫn Tắt Hệ Thống

*   **Tắt Web Python**: Nhấn tổ hợp phím `Ctrl + C` tại cửa sổ Terminal đang chạy `python main.py`.
*   **Tắt C# Microservices**: Đơn giản chỉ cần click nút **[X]** đóng 3 cửa sổ Console mới mở ra lúc chạy script.
