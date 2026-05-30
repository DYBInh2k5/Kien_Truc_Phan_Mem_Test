# KỊCH BẢN DEMO BẢO VỆ DỰ ÁN CHI TIẾT (DEMO GUIDE)
## HỆ THỐNG QUẢN LÝ ĐƠN HÀNG (OMS)

Tài liệu này cung cấp các lệnh khởi chạy nhanh nhất và kịch bản trình diễn (click-by-click) trên giao diện Frontend Web để bạn tự tin biểu diễn trước hội đồng phản biện.

---

## 🚀 1. LỆNH KHỞI CHẠY DỰ ÁN NHANH NHẤT

Mở **PowerShell** bằng quyền Administrator và chạy lần lượt các lệnh sau:

### Lệnh 1: Khởi chạy Web Component (FastAPI + Frontend + SQLite) bằng Docker
```powershell
cd "D:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Project\src\web_mvc"
docker-compose up -d --build
```
*(Chờ khoảng 10-15 giây để container khởi động và mở cổng 8000).*

### Lệnh 2: Khởi chạy cụm 3 C# Microservices (.NET Core)
```powershell
cd "D:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Project\src\microservices_csharp"
powershell -ExecutionPolicy Bypass -File .\run_microservices.ps1
```
*(Lệnh này sẽ tự động bật thêm 3 cửa sổ CMD chạy độc lập các cổng 5001, 5002, 5003).*

---

## 🎭 2. KỊCH BẢN TRÌNH DIỄN DEMO TỪNG BƯỚC (STEP-BY-STEP)

Sau khi khởi chạy thành công các lệnh trên, hãy mở trình duyệt web và truy cập địa chỉ: **`http://localhost:8000`**

### 📍 Bước 1: Giới thiệu giao diện tổng quan
*   **Thao tác**: Trình chiếu giao diện trang Web (SPA Dark Mode).
*   **Lời thoại**: *"Đây là giao diện chính của Hệ thống Quản lý Đơn hàng (OMS). Giao diện được thiết kế theo phong cách tối tối giản hiện đại. Ở góc phải tiêu đề, hệ thống hiển thị trạng thái **'SQLite Connected (Singleton)'** chứng minh kết nối Database thực thông qua Singleton Pattern đã được thiết lập thành công."*

### 📍 Bước 2: Demo chức năng Xác thực (Auth) & Đăng ký
*   **Thao tác**: 
    1. Điền vào Form đăng nhập: Tài khoản: `admin` / Mật khẩu: `123`. Bấm **Đăng Nhập**.
    2. Chỉ ra sự thay đổi trên Sidebar (Tên chuyển thành `admin`, quyền `Administrator`, nút Đăng xuất hiện ra).
    3. Nhấn **Đăng xuất**. Chọn tab **Đăng Ký** bên cạnh.
    4. Nhập Username mới: `khachhang1`, Email: `khach1@gmail.com`, Mật khẩu: `123`. Nhấn **Đăng ký**.
    5. Hệ thống báo đăng ký thành công. Chọn lại tab Đăng nhập và đăng nhập bằng tài khoản `khachhang1` mới tạo.
*   **Lời thoại**: *"Hệ thống hỗ trợ cơ chế xác thực JWT. Khi đăng nhập thành công, token được lưu vào LocalStorage của trình duyệt và Sidebar sẽ tự động cập nhật thông tin người dùng cùng quyền hạn. Khi đăng ký tài khoản mới, dữ liệu sẽ được lưu trực tiếp vào cơ sở dữ liệu SQLite."*

### 📍 Bước 3: Demo chức năng Quản lý thành viên (User Management)
*   **Thao tác**: Click chọn tab **Quản lý Users** trên Sidebar bên trái.
*   **Lời thoại**: *"Tại tab này, hệ thống sẽ thực hiện truy vấn trực tiếp từ bảng `users` trong SQLite và hiển thị lên bảng. Quý thầy cô có thể thấy tài khoản **khachhang1** chúng em vừa đăng ký ở bước trước đã xuất hiện trong danh sách với quyền hạn là USER."*

### 📍 Bước 4: Demo chức năng Đặt hàng (Facade + Factory + State)
*   **Thao tác**:
    1. Click chọn tab **Đặt hàng & Tra cứu** trên Sidebar.
    2. Tại Form Đặt hàng: Chọn sản phẩm là *MacBook Pro M3*.
    3. Chọn phương thức vận chuyển: Click chọn **Giao hàng hỏa tốc** (Express - Phí ship $15.0).
    4. Nhập địa chỉ nhận hàng: `123 Nguyễn Huệ, Quận 1`.
    5. Nhấn nút **Tiến hành đặt hàng (Facade Process)**.
    6. Chỉ ra thông báo Alert màu xanh lá cây xuất hiện bên dưới form.
*   **Lời thoại**: *"Khi chúng em nhấn đặt hàng, một chu trình phức tạp sẽ được chạy ngầm thông qua **Facade Pattern**. Facade này sẽ gọi **Factory Method** để khởi tạo đúng loại đơn hàng hỏa tốc (`ExpressOrder`) nhằm tính toán phí vận chuyển là $15. Lớp **State Pattern** (`OrderContext`) sẽ tự động luân chuyển trạng thái của đơn hàng từ Pending sang Paid và Shipped sau khi kiểm kho và thanh toán hoàn tất. Cuối cùng đơn hàng được chèn thành công vào SQLite với mã đơn hàng mới."*

### 📍 Bước 5: Demo chức năng Tìm kiếm & Duyệt danh sách (Iterator)
*   **Thao tác**:
    1. Tại ô Tìm kiếm đơn hàng bên tay phải, nhập ID đơn hàng vừa tạo (ví dụ: `103`). Nhấn nút **Tìm**.
    2. Giao diện hiển thị chi tiết thông tin đơn hàng vừa tìm được.
    3. Nhìn xuống bảng **Tất cả đơn hàng**, nhấn nút **Làm mới (Refresh)** để cập nhật danh sách đơn hàng mới nhất (trong đó có đơn hàng 103 vừa đặt).
*   **Lời thoại**: *"Chúng em có thể tìm kiếm đơn hàng vừa đặt bằng ID thông qua bộ lọc tìm kiếm. Logic tìm kiếm và liệt kê danh sách đơn hàng được áp dụng mẫu thiết kế **Iterator Pattern** trên collection `OrderCollection`, giúp duyệt qua tập hợp dữ liệu SQLite mà không để lộ cấu trúc lưu trữ nội bộ."*

### 📍 Bước 6: Trình diễn cụm C# Microservices độc lập
*   **Thao tác**: Mở các tab trình duyệt mới và truy cập các API C# sau:
    1. `http://localhost:5001/api/sso/verify?token=sso_token_secure_admin_xyz`
    2. `http://localhost:5002/api/search/orders/101`
    3. `http://localhost:5003/api/report/summary`
*   **Lời thoại**: *"Bên cạnh Web Component chính, cụm 3 Microservices viết bằng C# (.NET 8.0) của chúng em hoạt động hoàn toàn độc lập trên các cổng 5001, 5002, 5003. SSO Service thực hiện kiểm tra token, Search Service hỗ trợ tìm kiếm nâng cao, và Report Service trả về báo cáo thống kê định dạng JSON."*

### 📍 Bước 7: Trình diễn tính bền vững của Cơ sở dữ liệu (SQLite Persistence)
*   **Thao tác**:
    1. Quay lại cửa sổ PowerShell chạy Docker Web, tắt server bằng lệnh: `docker-compose down`.
    2. Truy cập lại `http://localhost:8000` -> Chỉ ra trang web không thể truy cập (đã tắt).
    3. Khởi động lại bằng lệnh: `docker-compose up -d`.
    4. Mở lại trình duyệt `http://localhost:8000` -> Đăng nhập lại -> Vào tab **Quản lý Users** và **Đặt hàng & Tra cứu**.
    5. Chỉ ra tài khoản `khachhang1` và đơn hàng ID `103` vừa tạo trước đó vẫn còn tồn tại nguyên vẹn.
*   **Lời thoại**: *"Cuối cùng, chúng em xin chứng minh dữ liệu được lưu trữ bền vững. Sau khi tắt hoàn toàn máy chủ Web Docker và khởi động lại, các dữ liệu tài khoản và đơn hàng mới được tạo vẫn tồn tại nguyên vẹn trong tệp SQLite, chứng minh việc tích hợp Database thật đã thành công."*
