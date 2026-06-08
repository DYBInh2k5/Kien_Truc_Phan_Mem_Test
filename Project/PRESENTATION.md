# HỆ THỐNG QUẢN LÝ ĐƠN HÀNG (OMS) - SLIDES OUTLINE & SPEECH NOTES

---

### SLIDE 1: TRANG TIÊU ĐỀ
*   **Tiêu đề**: HỆ THỐNG QUẢN LÝ ĐƠN HÀNG (OMS)
*   **Tiêu đề phụ**: Ứng dụng Kiến trúc Phân tầng n-Tier & C# Microservices kết hợp áp dụng 5 Design Patterns
*   **Môn học**: Kiến Trúc Phần Mềm (Software Architecture)
*   **Giảng viên hướng dẫn**: [Tên Giảng Viên]
*   **Nhóm thực hiện**: [Tên các thành viên]
*   **Đường dẫn Slide thuyết trình (Gamma App)**: [Gamma Presentation Link](https://gamma.app/docs/HE-THONG-QUAN-LY-ON-HANG-OMS-fafqe6v198xhdqx)
*   **Mã nguồn tổng quát**:
    *   Thư mục dự án: [Project Directory](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project)
*   **Lời thoại người nói**:
    > "Kính thưa quý thầy cô trong Hội đồng phản biện. Hôm nay, nhóm chúng em xin phép được trình bày báo cáo dự án môn học Kiến trúc phần mềm với đề tài: Hệ thống Quản lý Đơn hàng (OMS). Trong dự án này, chúng em tập trung giải quyết bài toán nghiệp vụ phức tạp của thương mại điện tử bằng cách kết hợp kiến trúc phân tầng n-Tier truyền thống với cụm Microservices hiện đại, đồng thời áp dụng 5 mẫu thiết kế (Design Patterns) kinh điển nhằm đạt được một hệ thống có tính Loose Coupling (kết nối lỏng lẻo), dễ bảo trì và dễ dàng mở rộng trong tương lai. Sau đây, chúng em xin đi vào chi tiết bài toán thực tế."

---

### SLIDE 2: MÔ TẢ BÀI TOÁN THỰC TẾ & THÁCH THỨC
*   **Nội dung trình chiếu**:
    *   Quy trình xử lý đơn hàng phức tạp (gồm nhiều subsystem: Kho hàng, Thanh toán, Giao hàng) dễ làm mã nguồn bị rối (Spaghetti code).
    *   Trạng thái đơn hàng biến động liên tục, nếu xử lý bằng cấu trúc `if/else` lồng nhau truyền thống sẽ rất khó mở rộng và dễ phát sinh lỗi khi thêm trạng thái mới.
    *   Dễ xảy ra lỗi nghẽn hoặc xung đột ghi đọc cơ sở dữ liệu khi có nhiều kết nối đồng thời.
*   **Lời thoại người nói**:
    > "Trong các hệ thống thương mại điện tử thực tế, quy trình xử lý đơn hàng là một trong những luồng nghiệp vụ phức tạp nhất. Nó yêu cầu sự tương tác liên tục của nhiều phân hệ khác nhau từ kiểm kho, xử lý thanh toán đến điều phối vận chuyển. Nếu lập trình theo phong cách tuần tự thông thường, mã nguồn sẽ trở nên cực kỳ phức tạp, tạo ra các lớp 'God Object' nắm giữ quá nhiều trách nhiệm. Hơn nữa, việc quản lý vòng đời đơn hàng với hàng loạt lệnh rẽ nhánh `if/else` sẽ biến mã nguồn thành Spaghetti code, rất khó để cập nhật hay sửa đổi. Để vượt qua các rào cản này, nhóm chúng em đề xuất một giải pháp kỹ thuật kết hợp cấu trúc phân tầng n-Tier kết hợp Microservice và 5 Design Patterns."

---

### SLIDE 3: KIẾN TRÚC HỆ THỐNG TỔNG THỂ
*   **Nội dung trình chiếu**:
    *   **Web Component (Python FastAPI)**: Viết theo mô hình MVC / n-Layers. Đóng vai trò là ứng dụng chính phục vụ Client và kết nối SQLite Database.
    *   **Microservices Component (C# .NET 8.0)**: Cụm 3 dịch vụ API độc lập phục vụ các tác vụ chuyên biệt:
        *   `SSOService` (Cổng 5001): Xác thực và cấp phát Token.
        *   `SearchService` (Cổng 5002): Tìm kiếm đơn hàng nâng cao.
        *   `ReportService` (Cổng 5003): Thống kê báo cáo đơn hàng.
    *   **Giao thức kết nối**: REST API (HTTP) truyền dữ liệu JSON.
*   **File mã nguồn liên quan**:
    *   Khởi động cụm dịch vụ C#: [run_microservices.ps1](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/microservices_csharp/run_microservices.ps1)
    *   Dockerfile của Web MVC: [Dockerfile](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/Dockerfile)
    *   File cấu hình Docker Compose: [docker-compose.yml](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/docker-compose.yml)
*   **Lời thoại người nói**:
    > "Đây là sơ đồ kiến trúc tổng thể của hệ thống. Chúng em phân chia dự án thành hai khối thành phần lớn: Khối thứ nhất là Web Component viết bằng Python FastAPI theo cấu trúc phân tầng n-Tier (MVC) kết nối với cơ sở dữ liệu SQLite thật. Khối thứ hai là cụm 3 Microservices viết bằng C# .NET 8.0 chạy độc lập trên các cổng 5001, 5002 và 5003. Khối Web Component giao tiếp chéo với cụm Microservices thông qua giao thức HTTP REST API gửi nhận dữ liệu JSON. Thiết kế này giúp hệ thống vừa tận dụng được sự gọn nhẹ của FastAPI trong làm giao diện, vừa đảm bảo hiệu năng xử lý tác vụ chuyên biệt của .NET."

---

### SLIDE 4: PHÂN TÍCH KIẾN TRÚC WEB COMPONENT (MVC / N-LAYERS)
*   **Nội dung trình chiếu**:
    *   **Controllers (API Routes)**: Tiếp nhận Request từ Client, điều hướng và thực hiện proxy gọi C# Service.
    *   **Services Layer**: Chứa Business Logic (Quy trình xác thực, nghiệp vụ đơn hàng).
    *   **Patterns Layer**: Nơi áp dụng các Design Patterns để xử lý logic sạch sẽ.
    *   **Repositories / Config (SQLite)**: Thực hiện đọc/ghi dữ liệu bền vững (Persistent Data) bằng SQLite thông qua kết nối Singleton.
*   **File mã nguồn liên quan**:
    *   Controller chính định tuyến API: [api_router.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/controllers/api_router.py)
    *   Service xử lý nghiệp vụ xác thực: [auth_service.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/services/auth_service.py)
    *   File Database SQLite vật lý: [orders.db](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/orders.db)
*   **Lời thoại người nói**:
    > "Đi sâu vào kiến trúc của Web Component, chúng em áp dụng mô hình phân tầng n-Tier nghiêm ngặt để đảm bảo nguyên lý Single Responsibility (Đơn trách nhiệm). Tầng View sử dụng Single Page Application viết bằng Vanilla CSS và JS không dùng framework cồng kềnh nhằm tối ưu tốc độ tải trang. Tầng Controller tiếp nhận request và định tuyến. Tầng Service Layer chịu trách nhiệm xử lý logic nghiệp vụ và tương tác với tầng Patterns. Cuối cùng, tầng Data Layer thực hiện truy vấn xuống database SQLite thật, giúp dữ liệu của hệ thống được lưu trữ bền vững lâu dài."

---

### SLIDE 5: MẪU THIẾT KẾ 1: SINGLETON PATTERN
*   **Nội dung trình chiếu**:
    *   **Lớp áp dụng**: `DatabaseConnection` kết nối SQLite.
    *   **Cách thức hoạt động**:
        *   Sử dụng cơ chế Double-Checked Locking kết hợp `threading.Lock()` để đảm bảo an toàn đa luồng (Thread-safe) trong môi trường Web API.
        *   Chỉ tạo duy nhất 1 instance kết nối tới SQLite `orders.db` trong suốt vòng đời ứng dụng.
    *   **Lợi ích**: Tiết kiệm tài nguyên CPU/RAM, tránh xung đột ghi/đọc (Database Lock) của SQLite.
*   **File mã nguồn liên quan**:
    *   File cài đặt Pattern: [singleton.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/singleton.py) (Dòng 6-25 chứa cấu trúc Singleton; dòng 27-74 chứa hàm khởi tạo DB mẫu; dòng 76-105 chứa các hàm truy vấn `query` và `execute`).
    *   Nơi sử dụng trong Controller: [api_router.py#L37](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/controllers/api_router.py#L37) (Gọi kết nối DB để ghi đơn hàng mới).
*   **Lời thoại người nói**:
    > "Mẫu thiết kế đầu tiên nhóm áp dụng là Singleton Pattern cho lớp quản lý kết nối cơ sở dữ liệu DatabaseConnection. Trong môi trường Web API, có hàng trăm yêu cầu đọc/ghi dữ liệu gửi tới đồng thời. Nếu mỗi request lại tạo ra một kết nối SQLite mới, tài nguyên hệ thống sẽ nhanh chóng bị cạn kiệt và xảy ra lỗi 'Database is locked' của SQLite. Với Singleton kết hợp cơ chế kiểm tra kép Double-Checked Locking và Thread-lock, chúng em đảm bảo toàn bộ hệ thống chỉ duy trì duy nhất một kết nối an toàn trong suốt vòng đời chạy ứng dụng."

---

### SLIDE 6: MẪU THIẾT KẾ 2: FACTORY METHOD PATTERN
*   **Nội dung trình chiếu**:
    *   **Lớp áp dụng**: `OrderFactory` tính toán và tạo đơn hàng.
    *   **Thực thể**:
        *   Lớp cha trừu tượng `Order`.
        *   Các lớp con cụ thể: `StandardOrder` (phí ship $2.5) và `ExpressOrder` (phí ship $15.0).
    *   **Lợi ích**: Giúp che giấu logic khởi tạo đối tượng phức tạp. Dễ dàng thêm các loại đơn hàng mới (Giao hàng bằng robot, giao hàng quốc tế) mà không làm ảnh hưởng tới code cũ.
*   **File mã nguồn liên quan**:
    *   File cài đặt Pattern: [factory.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/factory.py) (Dòng 5-15: Giao diện `Order`; dòng 18-30: Các Class cụ thể; dòng 33-44: Lớp `OrderFactory`).
    *   Nơi sử dụng trong Facade: [facade.py#L38](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/facade.py#L38) (Facade gọi Factory để tạo đúng instance đơn hàng và tính phí vận chuyển động).
*   **Lời thoại người nói**:
    > "Tiếp theo là Factory Method Pattern. Khi đặt hàng, phí vận chuyển và quy trình sẽ phụù thuộc vào phương thức giao hàng mà người dùng chọn (Giao hàng thường hoặc giao hỏa tốc). Chúng em đã định nghĩa một lớp cha trừu tượng là Order, và các lớp con cụ thể như StandardOrder và ExpressOrder. Lớp OrderFactory đóng vai trò là nhà máy sản xuất, tự động khởi tạo đúng đối tượng đơn hàng tương ứng. Nhờ mẫu thiết kế này, nếu trong tương lai doanh nghiệp muốn mở rộng thêm phương thức giao hàng mới như giao hàng bằng máy bay hay drone, chúng em chỉ cần viết thêm lớp con kế thừa mà hoàn toàn không cần sửa đổi mã nguồn ở tầng Controller."

---

### SLIDE 7: MẪU THIẾT KẾ 3: FACADE PATTERN
*   **Nội dung trình chiếu**:
    *   **Lớp áp dụng**: `OrderFacade`.
    *   **Cách thức hoạt động**:
        *   Bao bọc 3 hệ thống con phức tạp bên dưới: `InventorySystem` (Kiểm kho), `PaymentSystem` (Thanh toán), và `ShippingSystem` (Vận chuyển).
        *   Cung cấp một phương thức đơn giản duy nhất cho Controller gọi: `place_order()`.
    *   **Lợi ích**: Giảm sự phụ thuộc (Loose Coupling) giữa Controller và các Subsystems. Client không cần biết chi tiết quy trình thanh toán hay gửi hàng hoạt động như thế nào.
*   **File mã nguồn liên quan**:
    *   File cài đặt Pattern: [facade.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/facade.py) (Dòng 7-20: Định nghĩa 3 hệ thống con giả lập; dòng 23-70: Lớp `OrderFacade` điều phối các bước).
    *   Nơi sử dụng trong Controller: [api_router.py#L32-L33](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/controllers/api_router.py#L32-L33) (Khởi tạo Facade và thực hiện đặt hàng).
*   **Lời thoại người nói**:
    > "Để đặt một đơn hàng thành công, hệ thống phải trải qua rất nhiều bước phức tạp: kiểm tra số lượng tồn kho của sản phẩm, thực hiện thanh toán chi phí đơn hàng, và điều phối vận đơn cho đơn vị vận chuyển. Thay vì để Controller giao tiếp trực tiếp với cả 3 phân hệ phức tạp này, chúng em áp dụng Facade Pattern thông qua lớp OrderFacade. Lớp này cung cấp một giao diện cực kỳ đơn giản là place_order(). Controller chỉ cần gọi hàm này, mọi logic nghiệp vụ phức tạp bên dưới sẽ được Facade âm thầm điều phối. Điều này giúp giảm độ phụ thuộc chéo (coupling) và làm mã nguồn ở Controller vô cùng gọn gàng."

---

### SLIDE 8: MẪU THIẾT KẾ 4: STATE PATTERN
*   **Nội dung trình chiếu**:
    *   **Lớp áp dụng**: `OrderContext` & `OrderState`.
    *   **Cách thức hoạt động**:
        *   Trạng thái đơn hàng được đóng gói thành các Class cụ thể kế thừa từ `OrderState`: `PendingState`, `PaidState`, `ShippedState`.
        *   Khi gọi phương thức `proceed()`, trạng thái hiện tại sẽ tự động cập nhật sang trạng thái tiếp theo trong vòng đời đơn hàng.
    *   **Lợi ích**: Loại bỏ hoàn toàn các khối lệnh `if-else` lồng nhau. Code dễ bảo trì và cập nhật thêm trạng thái mới một cách dễ dàng.
*   **File mã nguồn liên quan**:
    *   File cài đặt Pattern: [state.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/state.py) (Dòng 4-11: Interface `OrderState`; dòng 13-34: Các trạng thái kế thừa; dòng 36-53: Lớp `OrderContext` điều phối trạng thái hiện tại).
    *   Nơi cập nhật trạng thái trong Facade: [facade.py#L41](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/facade.py#L41) (Khởi tạo Context ở trạng thái `Pending`), [L54](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/facade.py#L54) (chuyển sang `Paid` sau khi thanh toán) và [L61](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/facade.py#L61) (chuyển sang `Shipped` sau khi giao hàng).
*   **Lời thoại người nói**:
    > "Quản lý vòng đời trạng thái đơn hàng luôn là một thách thức lớn. Thông thường, lập trình viên sẽ viết các hàm cập nhật trạng thái chứa đầy các câu lệnh if/else để kiểm tra điều kiện chuyển đổi. Nhóm chúng em đã giải quyết triệt để vấn đề này bằng cách áp dụng State Pattern. Trạng thái của đơn hàng được đóng gói thành các đối tượng riêng biệt như PendingState, PaidState và ShippedState. Lớp ngữ cảnh OrderContext chỉ cần gọi phương thức proceed(), đơn hàng sẽ tự động nâng cấp trạng thái một cách tuần tự và thông minh dựa trên logic đóng gói sẵn trong từng lớp trạng thái, giúp loại bỏ hoàn toàn spaghetti code."

---

### SLIDE 9: MẪU THIẾT KẾ 5: ITERATOR PATTERN
*   **Nội dung trình chiếu**:
    *   **Lớp áp dụng**: `OrderCollection` duyệt qua danh sách đơn hàng từ SQLite.
    *   **Cách thức hoạt động**:
        *   Cài đặt 2 phương thức chuẩn của Python `__iter__()` và `__next__()` trên tập hợp đơn hàng.
        *   Hỗ trợ phương thức tìm kiếm đơn hàng `find_order()`.
    *   **Lợi ích**: Cho phép duyệt qua danh sách đơn hàng bằng vòng lặp `for...in` thông thường mà không làm lộ cấu trúc mảng (`_orders`) lưu trữ bên trong ra ngoài.
*   **File mã nguồn liên quan**:
    *   File cài đặt Pattern: [iterator.py](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns/iterator.py) (Dòng 3-31: Cấu trúc của lớp `OrderCollection`).
    *   Sử dụng khi tra cứu đơn hàng cục bộ (Fallback): [api_router.py#L70-L75](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/controllers/api_router.py#L70-L75) (Nạp danh sách thô SQLite vào collection và dùng phương thức `find_order` sử dụng Iterator để tìm kiếm).
    *   Sử dụng khi hiển thị tất cả đơn hàng: [api_router.py#L89-L94](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/controllers/api_router.py#L89-L94) (Sử dụng vòng lặp list comprehension chuẩn để duyệt qua `OrderCollection`).
*   **Lời thoại người nói**:
    > "Mẫu thiết kế cuối cùng là Iterator Pattern, được cài đặt cho lớp tập hợp OrderCollection. Khi truy vấn danh sách đơn hàng từ cơ sở dữ liệu SQLite, dữ liệu được nạp vào đối tượng OrderCollection. Nhờ triển khai Iterator, tầng Controller có thể duyệt qua danh sách đơn hàng bằng vòng lặp for...in chuẩn mực hoặc thực hiện tìm kiếm đơn hàng thông qua hàm find_order(). Mẫu thiết kế này giúp che giấu cấu trúc dữ liệu lưu trữ nội bộ của collection, giúp cho việc thay đổi cấu trúc lưu trữ sau này (từ mảng sang cây hoặc bảng băm) hoàn toàn không ảnh hưởng đến mã nguồn sử dụng bên ngoài."

---

### SLIDE 10: SƠ ĐỒ SEQUENCE DIAGRAM (TRƯỚC & SAU KHI ÁP DỤNG PATTERN)
*   **Nội dung trình chiếu**:
    *   **Trước khi áp dụng**:
        *   Client/Controller phải liên hệ trực tiếp với từng Subsystem lẻ tẻ (kiểm kho, thanh toán, vận chuyển).
        *   Sử dụng if/else lồng nhau phức tạp ở Controller để đổi trạng thái đơn hàng.
    *   **Sau khi áp dụng (Facade + State)**:
        *   Client chỉ gọi duy nhất `OrderFacade.place_order()`.
        *   Facade tự gọi các Subsystem ngầm.
        *   `OrderContext` tự động chuyển trạng thái từ `PendingState` sang các trạng thái tiếp theo một cách tuần tự và trơn tru.
*   **Lời thoại người nói**:
    > "Nhìn vào sơ đồ Sequence này, quý thầy cô có thể thấy rõ sự khác biệt lớn về độ phức tạp khi có và không có các mẫu thiết kế. Khi chưa áp dụng, Controller phải tự gọi đến từng phân hệ và thực hiện kiểm tra trạng thái bằng if/else lồng nhau. Sau khi áp dụng Facade và State Pattern, Controller giao tiếp ở mức độ trừu tượng cao nhất. Nó chỉ gửi lệnh place_order() tới Facade, Facade tự phối hợp các hệ thống con bên dưới, và trạng thái đơn hàng luân chuyển tự động thông qua máy trạng thái, giúp giảm độ phức tạp và cô lập logic lỗi tối đa."

---

### SLIDE 11: TÍCH HỢP CHÉO & CƠ CHẾ DỰ PHÒNG FALLBACK
*   **Nội dung trình chiếu**:
    *   **Tương tác thực tế**: Gọi HTTP POST tới C# `SSOService` (:5001) để xác thực và HTTP GET tới C# `ReportService` (:5003) lấy báo cáo thống kê.
    *   **Cơ chế dự phòng Fallback**:
        *   C# Microservices **Online**: Hệ thống ưu tiên kết nối chéo gọi C# API lấy dữ liệu thực tế.
        *   C# Microservices **Offline**: FastAPI tự động chuyển dịch dự phòng xác thực qua SQLite cục bộ và hiển thị dữ liệu thống kê giả lập, giữ cho hệ thống hoạt động liên tục.
*   **File mã nguồn liên quan**:
    *   Đoạn gọi SSO + Fallback xác thực: [auth_service.py#L19-L66](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/services/auth_service.py#L19-L66) (Khối `try...except` bao bọc việc gọi cổng 5001; nếu lỗi thì nhảy vào khối SQLite cục bộ).
    *   Đoạn gọi Report + Fallback: [api_router.py#L104-L125](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/controllers/api_router.py#L104-L125) (Nếu Report Service C# offline, tự động trả về cấu trúc dữ liệu mock hợp lệ cho UI).
    *   Đoạn gọi Search + Fallback: [api_router.py#L55-L80](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/controllers/api_router.py#L55-L80) (Gọi C# cổng 5002, nếu offline dùng Iterator cục bộ).
*   **Lời thoại người nói**:
    > "Để dự án đạt được tính thực tế cao nhất của hệ thống phân tán, chúng em đã phát triển cơ chế tích hợp chéo. Khi người dùng đăng nhập hoặc xem báo cáo, FastAPI sẽ gửi yêu cầu HTTP trực tiếp tới các dịch vụ C# SSO cổng 5001 và Report cổng 5003. Đặc biệt, chúng em đã thiết kế cơ chế Fallback (dự phòng tự động). Nếu các dịch vụ C# Microservices gặp sự cố hoặc offline, hệ thống Python sẽ tự động bắt ngoại lệ kết nối và rơi vào cơ chế dự phòng cục bộ: sử dụng database SQLite để xác thực người dùng và hiển thị báo cáo mock cục bộ, giúp hệ thống không bao giờ bị gián đoạn hay crash ứng dụng."

---

### SLIDE 12: DEMO GIAO DIỆN WEB FRONTEND SPA & C# MICROSERVICES
*   **Nội dung trình chiếu**:
    *   **Giao diện SPA**: Premium Dark Mode sử dụng HTML/CSS/JS thuần kết nối AJAX, đồng bộ dữ liệu SQLite.
    *   **Chức năng chính**:
        *   Xác thực (JWT Token + SSO source indicator).
        *   Quản lý thành viên (Bảng dữ liệu SQLite).
        *   Đặt hàng qua Facade (Standard/Express).
        *   Tìm kiếm đơn hàng theo ID (Iterator).
    *   **Microservices C#**: 3 dịch vụ API độc lập kết nối liên thông hiển thị báo cáo thời gian thực.
*   **File mã nguồn liên quan**:
    *   C# SSOService cổng 5001: [SSOService/Program.cs](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/microservices_csharp/SSOService/Program.cs) (Nhận request login, xác minh SQLite và sinh Token).
    *   C# SearchService cổng 5002: [SearchService/Program.cs](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/microservices_csharp/SearchService/Program.cs) (Truy vấn đơn hàng theo ID từ SQLite).
    *   C# ReportService cổng 5003: [ReportService/Program.cs](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/microservices_csharp/ReportService/Program.cs) (Tính tổng đơn hàng, doanh thu thực tế bằng SQLite).
*   **Lời thoại người nói**:
    > "Tiếp theo, chúng em xin giới thiệu giao diện Web Frontend của ứng dụng. Giao diện được thiết kế theo phong cách Dark Mode cao cấp với bảng màu HSL hài hòa, ứng dụng các micro-animations tinh tế giúp trải nghiệm người dùng trở nên mượt mà. Hệ thống được tổ chức dạng Single Page Application (SPA), giúp người dùng chuyển đổi nhanh giữa các chức năng mà không cần tải lại trang. Các thông tin về cơ sở dữ liệu đang kết nối cũng như nguồn gốc của dữ liệu xác thực đều được hiển thị trực quan thông qua các huy hiệu trạng thái động trên thanh tiêu đề và thẻ Dashboard."

---

### SLIDE 13: KẾT LUẬN & BÀI HỌC RÚT RA
*   **Nội dung trình chiếu**:
    *   **Đạt được**: Áp dụng thành công 5 Design Patterns theo chuẩn thiết kế SOLID, Loose Coupling.
    *   **Tính thực tế**: Kết nối database SQLite thật và tích hợp liên thông hệ thống phân tán đa nền tảng (Python & C#).
    *   **Khả năng nâng cấp**: Cực kỳ dễ dàng thêm phương thức giao hàng, trạng thái đơn hàng hoặc các microservices mới.
*   **Lời thoại người nói**:
    > "Tóm lại, thông qua dự án OMS này, nhóm chúng em đã áp dụng thành công các nguyên lý thiết kế SOLID và các mẫu thiết kế mẫu mực vào thực tế. Hệ thống đạt được độ Loose Coupling cao, giúp tách biệt hoàn toàn trách nhiệm giữa giao diện, nghiệp vụ và các cổng dịch vụ microservices độc lập. Đây là nền tảng vững chắc để phát triển các hệ thống thương mại điện tử quy mô lớn. Nhóm chúng em xin chân thành cảm ơn thầy cô trong Hội đồng phản biện đã lắng nghe. Sau đây, chúng em xin phép được thực hiện phần Demo thực tế của ứng dụng và sẵn sàng tiếp nhận các câu hỏi phản biện."
