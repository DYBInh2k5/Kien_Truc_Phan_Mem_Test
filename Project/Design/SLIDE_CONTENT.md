# NỘI DUNG SLIDE THUYẾT TRÌNH BẢO VỆ BÀI TẬP LỚN
**Đề tài: Hệ thống Quản lý Đơn hàng (OMS) áp dụng 5 Design Patterns**

---

### 💻 Slide 1: Trang Tiêu Đề
*   **Tiêu đề lớn**: HỆ THỐNG QUẢN LÝ ĐƠN HÀNG (OMS)
*   **Tiêu đề phụ**: Ứng dụng Kiến trúc n-Tier & Tích hợp cụm C# Microservices kết hợp áp dụng 5 Design Patterns
*   **Môn học**: Kiến Trúc Phần Mềm (Software Architecture)
*   **Giảng viên hướng dẫn**: [Tên Giảng Viên]
*   **Nhóm thực hiện**: [Tên các thành viên]

---

### 💻 Slide 2: Mô Tả Bài Toán Thực Tế (Problem Description)
*   **Thách thức của hệ thống truyền thống**:
    *   Quy trình xử lý đơn hàng phức tạp (gồm nhiều subsystem: Kho, Thanh toán, Vận chuyển) dễ làm mã nguồn bị rối (Spaghetti code).
    *   Trạng thái đơn hàng biến động liên tục, nếu xử lý bằng cấu trúc `if/else` truyền thống sẽ rất khó mở rộng và dễ phát sinh lỗi khi thêm trạng thái mới.
    *   Hệ thống phình to, thiếu tính module hóa và không tối ưu hóa tài nguyên kết nối Database.
*   **Giải pháp**: Xây dựng kiến trúc phân tầng (n-Tier) kết hợp cấu trúc Microservice và áp dụng 5 mẫu thiết kế (Design Patterns) kinh điển để module hóa hệ thống.

---

### 💻 Slide 3: Kiến Trúc Hệ Thống Tổng Thể
*   **Gồm 2 thành phần chính**:
    1.  **Web Component (Python FastAPI)**: Viết theo mô hình MVC / n-Layers. Đóng vai trò là ứng dụng chính phục vụ Client và kết nối SQLite Database.
    2.  **Microservices Component (C# .NET 8.0)**: Cụm 3 dịch vụ API độc lập phục vụ các tác vụ chuyên biệt:
        *   `SSOService` (Cổng 5001): Xác thực và cấp phát Token.
        *   `SearchService` (Cổng 5002): Tìm kiếm đơn hàng nâng cao.
        *   `ReportService` (Cổng 5003): Thống kê báo cáo đơn hàng.
*   **Giao thức kết nối**: REST API (HTTP) truyền dữ liệu JSON.

---

### 💻 Slide 4: Tầng Web Component: Mô hình MVC / n-Layers
*   **Controllers (API Routes)**: Tiếp nhận Request từ Client Frontend, điều hướng và gọi các dịch vụ xử lý.
*   **Services Layer**: Chứa Business Logic (Quy trình xác thực, nghiệp vụ đơn hàng).
*   **Patterns Layer**: Nơi áp dụng các Design Patterns để xử lý logic sạch sẽ.
*   **Repositories / Config (SQLite)**: Thực hiện đọc/ghi dữ liệu bền vững (Persistent Data) bằng SQLite thông qua kết nối Singleton.

---

### 💻 Slide 5: Mẫu Thiết Kế 1: Singleton (Creational Group)
*   **Lớp áp dụng**: `DatabaseConnection` (tại [singleton.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/singleton.py))
*   **Cách thức hoạt động**:
    *   Sử dụng cơ chế **Double-Checked Locking** kết hợp `threading.Lock()` để đảm bảo an toàn đa luồng (Thread-safe) trong môi trường Web API.
    *   Chỉ tạo duy nhất 1 instance kết nối tới SQLite `orders.db` trong suốt vòng đời ứng dụng.
*   **Lợi ích**: Tiết kiệm tài nguyên CPU/RAM, tránh xung đột ghi/đọc (Database Lock) của SQLite.

---

### 💻 Slide 6: Mẫu Thiết Kế 2: Factory Method (Creational Group)
*   **Lớp áp dụng**: `OrderFactory` (tại [factory.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/factory.py))
*   **Cách thức hoạt động**:
    *   Định nghĩa lớp trừu tượng `Order` với các hàm `get_shipping_cost()` và `get_order_type()`.
    *   Các lớp con cụ thể: `StandardOrder` (phí ship $2.5) và `ExpressOrder` (phí ship $15.0).
    *   `OrderFactory` tự động phân tích tham số để khởi tạo đối tượng lớp con tương ứng.
*   **Lợi ích**: Giúp che giấu logic khởi tạo đối tượng phức tạp. Dễ dàng thêm các loại đơn hàng mới (Giao hàng bằng robot, giao hàng quốc tế) mà không làm ảnh hưởng tới code cũ.

---

### 💻 Slide 7: Mẫu Thiết Kế 3: Facade (Structural Group)
*   **Lớp áp dụng**: `OrderFacade` (tại [facade.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/facade.py))
*   **Cách thức hoạt động**:
    *   Bao bọc 3 hệ thống con phức tạp bên dưới: `InventorySystem` (Kiểm kho), `PaymentSystem` (Thanh toán), và `ShippingSystem` (Vận chuyển).
    *   Cung cấp một phương thức đơn giản duy nhất cho Controller gọi: `place_order()`.
*   **Lợi ích**: Giảm sự phụ thuộc (Loose Coupling) giữa Controller và các Subsystems. Client không cần biết chi tiết quy trình thanh toán hay gửi hàng hoạt động như thế nào.

---

### 💻 Slide 8: Mẫu Thiết Kế 4: State Pattern (Behavioral Group)
*   **Lớp áp dụng**: `OrderContext` & `OrderState` (tại [state.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/state.py))
*   **Cách thức hoạt động**:
    *   Trạng thái đơn hàng được đóng gói thành các Class cụ thể kế thừa từ `OrderState`: `PendingState`, `PaidState`, `ShippedState`.
    *   Khi gọi phương thức `proceed()`, trạng thái hiện tại sẽ tự động cập nhật sang trạng thái tiếp theo trong vòng đời đơn hàng.
*   **Lợi ích**: Loại bỏ hoàn toàn các khối lệnh `if-else` lồng nhau. Code dễ bảo trì và cập nhật thêm trạng thái mới một cách dễ dàng.

---

### 💻 Slide 9: Mẫu Thiết Kế 5: Iterator Pattern (Behavioral Group)
*   **Lớp áp dụng**: `OrderCollection` (tại [iterator.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/iterator.py))
*   **Cách thức hoạt động**:
    *   Cài đặt 2 phương thức đặc biệt của Python `__iter__()` và `__next__()` trên tập hợp đơn hàng.
    *   Hỗ trợ phương thức tìm kiếm đơn hàng `find_order()`.
*   **Lợi ích**: Cho phép duyệt qua danh sách đơn hàng (hoặc thông tin đối tượng) bằng vòng lặp `for...in` thông thường mà không cần phơi bày cấu trúc mảng (`_orders`) lưu trữ bên trong ra ngoài.

---

### 💻 Slide 10: Sơ đồ Sequence Diagram (Trước & Sau khi áp dụng Pattern)
*   **Trước khi áp dụng**:
    *   Client/Controller phải liên hệ trực tiếp với từng Subsystem lẻ tẻ (kiểm kho, thanh toán, vận chuyển).
    *   Sử dụng if/else lồng nhau phức tạp ở Controller để đổi trạng thái đơn hàng.
*   **Sau khi áp dụng (Facade + State)**:
    *   Client chỉ gọi duy nhất `OrderFacade.place_order()`.
    *   Facade tự gọi các Subsystem ngầm.
    *   `OrderContext` tự động chuyển trạng thái từ `PendingState` sang các trạng thái tiếp theo một cách tuần tự và trơn tru.

---

### 💻 Slide 11: Demo Giao Diện Web Frontend (SPA)
*   **Thiết kế Giao diện**: Sleek Dark Mode (chế độ tối hiện đại), trực quan, tối ưu trải nghiệm.
*   **Các chức năng trình diễn**:
    1.  **Xác thực (Auth)**: Biểu mẫu Đăng nhập/Đăng ký lưu token JWT vào LocalStorage.
    2.  **Quản lý người dùng (CRUD)**: Danh sách User đồng bộ từ SQLite.
    3.  **Đặt hàng (Facade)**: Chọn loại đơn hàng Standard/Express và địa chỉ.
    4.  **Theo dõi & Tìm kiếm**: Tìm kiếm đơn hàng theo ID qua Iterator.
    5.  **Bảng điều khiển (Dashboard)**: Thống kê số lượng đơn hàng theo trạng thái.

---

### 💻 Slide 12: Demo Cụm C# Microservices
*   **Đặc điểm kỹ thuật**: Xây dựng bằng ASP.NET Core Web API (Minimal APIs) cực kỳ nhẹ.
*   **Các Service chạy độc lập**:
    *   `SSOService` (Cổng 5001): Endpoint `/api/sso/login` & `/api/sso/verify`.
    *   `SearchService` (Cổng 5002): Tìm kiếm đơn hàng nâng cao `/api/search/orders/{id}`.
    *   `ReportService` (Cổng 5003): Thống kê báo cáo `/api/report/summary`.
*   **Khởi chạy nhanh chóng**: Script PowerShell `run_microservices.ps1` tự động bật 3 cửa sổ console riêng biệt phục vụ việc demo nhanh trước hội đồng chấm thi.

---

### 💻 Slide 13: Kết Luận & Câu Hỏi Phản Biện Gợi Ý
*   **Những giá trị đạt được**:
    *   Ứng dụng thiết kế theo chuẩn SOLID.
    *   Hệ thống có tính Loose Coupling (kết nối lỏng lẻo), dễ bảo trì và nâng cấp.
    *   Khả năng mở rộng cao nhờ phân tách cụm Web và Microservices C#.
*   **Các câu hỏi phản biện hội đồng thường hỏi**:
    *   *Câu 1*: Singleton của bạn có thực sự an toàn trong môi trường đa luồng không? -> Trả lời: Có, sử dụng khóa Lock bảo vệ và cơ chế kiểm tra kép Double-Checked Locking.
    *   *Câu 2*: Tại sao bạn sử dụng Facade Pattern cho việc đặt hàng? -> Trả lời: Vì quy trình đặt hàng liên quan tới nhiều subsystem (kiểm kho, thanh toán, vận chuyển), Facade giúp gom nhóm các xử lý này lại thành một giao diện đơn giản cho Controller dễ tương tác.
