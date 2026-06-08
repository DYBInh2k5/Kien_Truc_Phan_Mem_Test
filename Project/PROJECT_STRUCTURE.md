# 🗺️ BẢN ĐỒ KIẾN TRÚC & PHÂN CHIA TRÁCH NHIỆM HỆ THỐNG (PROJECT STRUCTURE & RESPONSIBILITY MAP)
## HỆ THỐNG QUẢN LÝ ĐƠN HÀNG (OMS) - SOFTWARE ARCHITECTURE

Tài liệu này tổng hợp chi tiết cấu trúc phân rã của toàn bộ dự án, trách nhiệm cụ thể của từng phân hệ, từng tệp tin và luồng dữ liệu đi qua các Design Patterns & Microservices để phục vụ việc giải trình trước Hội đồng chấm thi.

---

## 📑 MỤC LỤC
1. [CẤU TRÚC PHÂN RÃ THƯ MỤC CHI TIẾT (FOLDER BREAKDOWN)](#1-cấu-trúc-phân-rã-thư-mục-chi-tiết-folder-breakdown)
2. [BẢN ĐỒ PHÂN CHIA TRÁCH NHIỆM CHỨC NĂNG (WHO DOES WHAT)](#2-bản-đồ-phân-chia-trách-nhiệm-chức-năng-who-does-what)
3. [SƠ ĐỒ LUỒNG ĐI CỦA DỮ LIỆU THỜI GIAN THỰC (DATA FLOW)](#3-sơ-đồ-luồng-đi-của-dữ-liệu-thời-gian-thực-data-flow)
4. [TÓM TẮT GIẢI TRÌNH ĐỂ TRẢ LỜI CÂU HỎI CỦA THẦY CÔ](#4-tóm-tắt-giải-trình-để-trả-lời-câu-hỏi-của-thầy-cô)

---

## 1. CẤU TRÚC PHÂN RÃ THƯ MỤC CHI TIẾT (FOLDER BREAKDOWN)

Dự án được tổ chức theo mô hình kết hợp: **Kiến trúc phân tầng n-Tier (MVC)** ở Web chính và **Kiến trúc Microservices** ở các dịch vụ phụ trợ.

```text
Project/
│
├── Project_Structure.md               <-- File này (Bản đồ kiến trúc)
├── FinalProject.md                    <-- Checklist yêu cầu bài tập lớn
├── Readme.md                          <-- Giới thiệu chung dự án
├── RUN_GUIDE.md                       <-- Hướng dẫn cài đặt & khởi chạy nhanh
├── DEMO_GUIDE.md                      <-- Cẩm nang demo click-by-click và thoại mẫu
├── PRESENTATION.md                    <-- Dàn ý nội dung 13 slides và lời thoại
├── PRESENTATION_GUIDE.md              <-- Kịch bản thuyết trình & 15 câu hỏi phản biện
│
└── src/                               <-- Thư mục chứa toàn bộ mã nguồn
    │
    ├── web_mvc/                       <-- PHÂN HỆ 1: Web Component chính (FastAPI + SQLite)
    │   ├── Dockerfile                 <-- Định nghĩa Container đóng gói FastAPI Web
    │   ├── docker-compose.yml         <-- Cấu hình chạy Container mvc_project_web cổng 8000
    │   ├── main.py                    <-- Điểm khởi chạy FastAPI Web Server
    │   ├── orders.db                  <-- Tệp cơ sở dữ liệu SQLite vật lý dùng chung
    │   ├── requirements.txt           <-- Danh sách thư viện Python phụ thuộc
    │   │
    │   └── app/                       <-- Cấu trúc phân tầng n-Tier (MVC) của Web chính
    │       ├── controllers/
    │       │   └── api_router.py      <-- TẦNG CONTROLLER: Định tuyến request, gọi API Proxy và xử lý Fallback
    │       │
    │       ├── models/                <-- TẦNG DATA MODEL (DTOs): Định nghĩa cấu trúc dữ liệu gửi/nhận
    │       │   ├── order.py
    │       │   └── user.py
    │       │
    │       ├── services/
    │       │   └── auth_service.py    <-- TẦNG SERVICE: Logic nghiệp vụ xác thực thành viên
    │       │
    │       ├── patterns/              <-- TẦNG DESIGN PATTERNS: Đóng gói các mẫu thiết kế cốt lõi
    │       │   ├── singleton.py       <-- Lớp DatabaseConnection (Singleton kết nối SQLite)
    │       │   ├── factory.py         <-- Lớp OrderFactory, StandardOrder, ExpressOrder (Factory Method)
    │       │   ├── facade.py          <-- Lớp OrderFacade (Facade điều phối Kho - Thanh toán - Giao vận)
    │       │   ├── state.py           <-- Lớp OrderContext, PendingState, PaidState, ShippedState (State Pattern)
    │       │   └── iterator.py        <-- Lớp OrderCollection (Iterator duyệt và tìm kiếm đơn hàng)
    │       │
    │       └── static/                <-- TẦNG VIEW: Giao diện Single Page Application (SPA Dark Mode)
    │           ├── index.html         <-- Cấu trúc giao diện HTML
    │           ├── index.css          <-- Thiết kế hệ màu Slate/Dark Mode cao cấp bằng CSS
    │           └── app.js             <-- Logic tương tác AJAX/DOM thời gian thực
    │
    └── microservices_csharp/          <-- PHÂN HỆ 2: Cụm 3 Microservices viết bằng C# .NET 8.0
        ├── run_microservices.ps1      <-- Script khởi chạy đồng loạt 3 dịch vụ dưới dạng 3 cửa sổ CMD
        │
        ├── SSOService/                <-- MICROSERVICE 1 (Port 5001): Xác thực người dùng tập trung
        │   ├── Program.cs             <-- Khởi chạy API, tự động resolve orders.db, truy vấn SQLite
        │   └── SSOService.csproj
        │
        ├── SearchService/             <-- MICROSERVICE 2 (Port 5002): Tìm kiếm đơn hàng nâng cao
        │   ├── Program.cs             <-- API tìm kiếm đơn hàng trong SQLite
        │   └── SearchService.csproj
        │
        └── ReportService/             <-- MICROSERVICE 3 (Port 5003): Báo cáo thống kê tài chính
            ├── Program.cs             <-- API đọc SQLite, tính tổng doanh thu động
            └── ReportService.csproj
```

---

## 2. BẢN ĐỒ PHÂN CHIA TRÁCH NHIỆM CHỨC NĂNG (WHO DOES WHAT)

Khi thầy cô trong Hội đồng hỏi về một chức năng cụ thể và yêu cầu chỉ ra thành phần nào đảm nhiệm, bạn hãy đối chiếu theo bảng phân chia trách nhiệm nghiệp vụ dưới đây:

### 🔐 Chức năng Đăng ký & Đăng nhập thành viên
*   **Khi Microservices C# Online (Chế độ tích hợp)**:
    *   **Thao tác đăng nhập**: Người dùng điền thông tin đăng nhập trên giao diện [app.js](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/static/app.js) $\rightarrow$ Gửi request tới [api_router.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/controllers/api_router.py) của FastAPI $\rightarrow$ FastAPI chuyển yêu cầu làm Proxy sang **C# `SSOService` (Cổng 5001)** $\rightarrow$ Dịch vụ C# [SSOService/Program.cs](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/microservices_csharp/SSOService/Program.cs) mở database `orders.db` dùng chung để kiểm tra tài khoản và trả về Token.
*   **Khi Microservices C# Offline (Chế độ dự phòng Fallback)**:
    *   FastAPI nhận diện lỗi kết nối trong `auth_service.py` $\rightarrow$ Tự động Fallback sang gọi đối tượng [DatabaseConnection (Singleton)](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/singleton.py) để truy vấn trực tiếp bảng `users` trong SQLite cục bộ.

### 📦 Chức năng Đặt đơn hàng mới
*   Do **Web chính (FastAPI MVC)** đảm nhiệm 100% bằng cách phối hợp 4 mẫu thiết kế:
    *   [api_router.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/controllers/api_router.py#L29-L45) tiếp nhận dữ liệu và chuyển cho [OrderFacade](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/facade.py) (Facade).
    *   Facade gọi [OrderFactory](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/factory.py) (Factory Method) để tính phí vận chuyển của Standard/Express.
    *   Facade chuyển đổi trạng thái bằng [OrderContext](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/state.py) (State).
    *   Controller chèn dòng đơn hàng mới vào SQLite thông qua [DatabaseConnection](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/singleton.py) (Singleton).

### 📊 Chức năng Báo cáo thống kê Dashboard
*   **Khi C# Report Service Online**:
    *   Do **C# `ReportService` (Cổng 5003)** đảm nhiệm. Dịch vụ này chạy trên Windows Host, đọc bảng `orders` của SQLite để tính toán tổng số đơn, phân loại loại ship và cộng dồn doanh thu động (MacBook M3 = $2000, iPhone 15 Pro = $1200, Bàn phím Leopold = $150).
*   **Khi C# Report Service Offline**:
    *   FastAPI Web tự động bắt lỗi và Fallback bằng cách trả về dữ liệu thống kê giả lập (mock data) cục bộ để hiển thị lên Dashboard mà không gây lỗi giao diện.

### 🔍 Chức năng Tìm kiếm / Tra cứu đơn hàng
*   **Khi C# Search Service Online**:
    *   Do **C# `SearchService` (Cổng 5002)** đảm nhiệm. Quét bảng `orders` SQLite và trả về thông tin đơn hàng cùng chữ xác minh `(Đã xác minh qua C# Search)`.
*   **Khi C# Search Service Offline**:
    *   FastAPI Web tự động Fallback sang cục bộ: Đọc SQLite, đưa vào bộ sưu tập [OrderCollection](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/iterator.py) và tìm kiếm tuần tự bằng bộ duyệt **Iterator Pattern**.

---

## 3. SƠ ĐỒ LUỒNG ĐI CỦA DỮ LIỆU THỜI GIAN THỰC (DATA FLOW)

Dưới đây là luồng đi chi tiết của dữ liệu trong 2 tác vụ chính: **Đặt hàng** (ghi dữ liệu) và **Thống kê báo cáo** (đọc dữ liệu).

### 3.1 Luồng dữ liệu khi người dùng đặt hàng mới (Write Flow)
```mermaid
sequenceDiagram
    autonumber
    actor User as Khách Hàng
    participant SPA as Giao diện Web (SPA js)
    participant Router as API Router (Python FastAPI)
    participant Facade as OrderFacade (Facade)
    participant Factory as OrderFactory (Factory Method)
    participant State as OrderContext (State Pattern)
    participant Singleton as DatabaseConnection (Singleton)
    database SQLite as orders.db (SQLite file)

    User->>SPA: Nhấp "Tiến hành đặt hàng"
    SPA->>Router: Gửi POST /orders/place (JSON dữ liệu sản phẩm, địa chỉ)
    Router->>Facade: Gọi place_order(productId, type, address)
    Facade->>Factory: Gọi create_order(productId, type)
    Note over Factory: Khởi tạo StandardOrder hoặc ExpressOrder<br/>tính phí vận chuyển động
    Factory-->>Facade: Trả về thực thể Order
    Facade->>State: Khởi tạo OrderContext (Mặc định: PendingState)
    Note over Facade: Gọi kiểm kho (InventorySystem) &<br/>Gọi thanh toán (PaymentSystem)
    Facade->>State: Gọi proceed() (Chuyển trạng thái sang PaidState)
    Note over Facade: Gọi vận chuyển (ShippingSystem) sinh mã tracking
    Facade->>State: Gọi proceed() (Chuyển trạng thái sang ShippedState)
    Facade-->>Router: Trả về kết quả (Success, final_state=Shipped, tracking_code)
    Router->>Singleton: Gọi execute(INSERT INTO orders...)
    Singleton->>SQLite: Ghi trực tiếp bản ghi vào ổ đĩa
    Singleton-->>Router: Trả về new_order_id
    Router-->>SPA: Trả về JSON kết quả đặt hàng hoàn tất
    SPA-->>User: Hiển thị thông báo "Đặt hàng thành công!"
```

### 3.2 Luồng dữ liệu khi lấy báo cáo doanh thu tài chính (Read Flow)
```mermaid
sequenceDiagram
    autonumber
    actor User as Khách Hàng
    participant SPA as Giao diện Web (SPA js)
    participant Router as API Router (Python FastAPI)
    participant CSharp as C# ReportService (:5003)
    database SQLite as orders.db (SQLite file)

    User->>SPA: Nhấp vào tab Dashboard (hoặc nút Lấy báo cáo)
    SPA->>Router: Gửi GET /report/csharp-summary
    
    alt Trường hợp C# Microservice ONLINE
        Router->>CSharp: Gửi yêu cầu HTTP GET tới cổng 5003
        CSharp->>SQLite: Thực thi SELECT details FROM orders
        SQLite-->>CSharp: Trả về danh sách đơn hàng thực tế
        Note over CSharp: Quét danh sách, bóc tách giá trị sản phẩm<br/>và phí vận chuyển tương ứng để cộng dồn doanh thu
        CSharp-->>Router: Trả về JSON (total_orders, total_revenue) kèm nguồn C# Report
    else Trường hợp C# Microservice OFFLINE (Fallback)
        Note over Router: Bắt kết nối lỗi (Connection Refused)
        Note over Router: Kích hoạt Fallback cục bộ
        Router-->>Router: Sinh dữ liệu Mock báo cáo cục bộ
    end
    
    Router-->>SPA: Trả về kết quả thống kê doanh thu tài chính
    SPA-->>User: Render số liệu lên Dashboard kèm nhãn nguồn tương ứng
```

---

## 4. TÓM TẮT GIẢI TRÌNH ĐỂ TRẢ LỜI CÂU HỎI CỦA THẦY CÔ

Dưới đây là cẩm nang giúp bạn "phản xạ nhanh" khi thầy cô đặt câu hỏi về mặt kỹ thuật kiến trúc trong buổi bảo vệ:

*   **Câu hỏi 1: Tại sao cấu trúc dữ liệu SQLite chung lại nằm trong thư mục của Python Web? Hai bên kết nối như thế nào?**
    *   **Trả lời**: *"SQLite là cơ sở dữ liệu file cục bộ nằm tại `src/web_mvc/orders.db`. FastAPI Web chạy trong Docker nên nó mount thư mục chứa database này. Còn các Microservices C# chạy trực tiếp trên Windows Host, chúng em đã viết hàm giải quyết đường dẫn động duyệt ngược cây thư mục để trỏ đúng vào file `orders.db` của Python Web, giúp hai nền tảng cùng chia sẻ và đọc/ghi chung một cơ sở dữ liệu vật lý duy nhất, đảm bảo tính nhất quán dữ liệu thời gian thực."*

*   **Câu hỏi 2: Design Pattern nào đóng vai trò trung tâm của nghiệp vụ đặt hàng?**
    *   **Trả lời**: *"Dạ là **Facade Pattern** cài đặt ở `facade.py`. Lớp `OrderFacade` đóng vai trò là một mặt tiền quy tụ và điều phối 3 hệ thống con phức tạp là Kho hàng, Thanh toán và Vận chuyển. Thay vì bắt Controller phải gọi rời rạc 3 phân hệ này và tự quản lý luồng, Controller chỉ cần gọi duy nhất một phương thức `place_order()`. Ngoài ra, Facade này cũng là nơi điều hành việc khởi tạo đơn hàng từ **Factory Method** và luân chuyển vòng đời trạng thái của **State Pattern**."*

*   **Câu hỏi 3: Nếu dịch vụ C# SSO hoặc C# Report bị chết, ứng dụng có bị sập theo không?**
    *   **Trả lời**: *"Dạ hoàn toàn không. Chúng em thiết kế hệ thống theo nguyên tắc kết nối lỏng lẻo (Loose Coupling) và có thiết lập cơ chế **dự phòng tự động (Fallback)** trong các tệp tin Controller `api_router.py` và `auth_service.py`. Nếu C# sập, FastAPI tự động bắt exception và kích hoạt Fallback: tự xác thực qua SQLite cục bộ bằng Singleton Connection và tự hiển thị báo cáo mock dự phòng, giữ cho Web chính hoạt động liên tục 100% thời gian."*
