# TÀI LIỆU TỔNG HỢP TOÀN DIỆN DỰ ÁN (PROJECT DOCUMENTATION)
## HỆ THỐNG QUẢN LÝ ĐƠN HÀNG (OMS) - SOFTWARE ARCHITECTURE PROJECT

Dự án này là bài tập lớn kết thúc môn **Kiến trúc phần mềm (Software Architecture)**. 
Tài liệu này tích hợp toàn bộ các báo cáo thiết kế, hướng dẫn vận hành, kịch bản slide thuyết trình bảo vệ và các câu hỏi phản biện để sinh viên dễ dàng theo dõi và nộp bài.

---

## 📑 MỤC LỤC
1. [PHẦN 1: MÔ TẢ BÀI TOÁN & KHÁI QUÁT HỆ THỐNG](#phần-1-mô-tả-bài-toán--khái-quát-hệ-thống)
2. [PHẦN 2: THIẾT KẾ KIẾN TRÚC & SƠ ĐỒ HỆ THỐNG (DIAGRAMS)](#phần-2-thiết-kế-kiến-trúc--sơ-đồ-hệ-thống-diagrams)
3. [PHẦN 3: PHÂN TÍCH CHI TIẾT 5 DESIGN PATTERNS ÁP DỤNG](#phần-3-phân-tích-chi-tiết-5-design-patterns-áp-dụng)
4. [PHẦN 4: HƯỚNG DẪN TRIỂN KHAI & VẬN HÀNH (RUN GUIDE)](#phần-4-hướng-dẫn-triển-khai--vận-hành-run-guide)
5. [PHẦN 5: KỊCH BẢN NỘI DUNG 13 SLIDE THUYẾT TRÌNH BẢO VỆ](#phần-5-kịch-bản-nội-dung-13-slide-thuyết-trình-bảo-vệ)
6. [PHẦN 6: BỘ CÂU HỎI PHẢN BIỆN BẢO VỆ GỢI Ý (Q&A)](#phần-6-bộ-câu-hỏi-phản-biện-bảo-vệ-gợi-ý-qa)
7. [PHẦN 7: TÀI LIỆU API ĐẦY ĐỦ CHI TIẾT (API DOCUMENTATION)](#phần-7-tài-liệu-api-đầy-đủ-chi-tiết-api-documentation)
8. [PHẦN 8: HƯỚNG DẪN SỬA LỖI VÀ XỬ LÝ SỰ CỐ (TROUBLESHOOTING GUIDE)](#phần-8-hướng-dẫn-sửa-lỗi-và-xử-lý-sự-cố-troubleshooting-guide)
9. [PHẦN 9: KỊCH BẢN DEMO BẢO VỆ DỰ ÁN CHI TIẾT (DEMO GUIDE)](#phần-9-kịch-bản-demo-bảo-vệ-dự-án-chi-tiết-demo-guide)

---

---

## PHẦN 1: MÔ TẢ BÀI TOÁN & KHÁI QUÁT HỆ THỐNG

### 1. Mô tả bài toán thực tế (Problem Description)
Trong các doanh nghiệp thương mại điện tử hiện nay, hệ thống xử lý đơn hàng gặp thách thức lớn về tính bảo trì và mở rộng khi các quy trình nghiệp vụ trở nên phức tạp dần (phải liên kết với kho hàng để kiểm kho, liên kết với ngân hàng để thanh toán, liên kết với các đơn vị vận chuyển để giao hàng). 

Nếu sử dụng mã nguồn theo phong cách cấu trúc tuần tự hoặc dùng các lệnh `if/else` lồng nhau để quản lý trạng thái đơn hàng (Đang chờ duyệt -> Đã thanh toán -> Đang giao -> Hoàn tất), mã nguồn sẽ bị phình to (Spaghetti Code / God Object), dẫn đến cực kỳ khó bảo trì và dễ phát sinh lỗi khi bổ sung các phương thức giao hàng hoặc trạng thái đơn hàng mới.

### 2. Giải pháp kỹ thuật
Hệ thống OMS được xây dựng trên sự kết hợp của:
*   **Kiến trúc phân tầng n-Tier (MVC)**: Phân tách rõ ràng giữa giao diện người dùng (View), tầng điều hướng (Controller), tầng xử lý nghiệp vụ (Service & Patterns) và tầng cơ sở dữ liệu SQLite (Repository).
*   **Kiến trúc Microservices**: Tích hợp các cổng dịch vụ độc lập viết bằng C# để xử lý các nghiệp vụ phụ như Xác thực tập trung (SSO), Tìm kiếm nâng cao (Search) và Thống kê báo cáo (Report).
*   **Áp dụng 5 Design Patterns mẫu mực**: Singleton, Factory Method, Facade, State, và Iterator giúp tối ưu hóa kết nối DB, module hóa logic khởi tạo, tối giản hóa giao thức giao tiếp và tự động quản lý vòng đời đơn hàng sạch sẽ.

---

## PHẦN 2: THIẾT KẾ KIẾN TRÚC & SƠ ĐỒ HỆ THỐNG (DIAGRAMS)

### 2.1 Sơ đồ Kiến trúc & Triển khai Hệ thống (Tích hợp 5+ Design Patterns)
Sơ đồ dưới đây mô tả chi tiết kiến trúc phân tầng n-Tier (Web Component FastAPI MVC) được đóng gói trong container Docker và cách nó tích hợp **5+ Design Patterns** (Singleton, Factory Method, Facade, State, Iterator, Proxy Gateway) để giao tiếp hiệu quả với cơ sở dữ liệu SQLite và cụm Microservices C# chạy trên máy host.

```mermaid
graph TB
    classDef client fill:#d4ebf2,stroke:#1a73e8,stroke-width:2px;
    classDef container fill:#fcfcfc,stroke:#5f6368,stroke-width:2px,stroke-dasharray: 5 5;
    classDef component fill:#e8f0fe,stroke:#1a73e8,stroke-width:2px;
    classDef pattern fill:#fef7e0,stroke:#f9ab00,stroke-width:2px;
    classDef db fill:#e6f4ea,stroke:#137333,stroke-width:2px;
    classDef service fill:#fce8e6,stroke:#c5221f,stroke-width:2px;

    Client((Client App / Browser)):::client

    subgraph Web_Application_Docker_Container ["Web Application Container (FastAPI MVC - Port 8000)"]
        
        subgraph Controller_Layer ["Controller Layer"]
            api_router[api_router.py<br/><i>(Proxy Gateway Pattern)</i>]:::component
        end

        subgraph Business_Logic_Service_Layer ["Business Logic & Design Patterns Layer"]
            facade[OrderFacade<br/><b>[Facade Pattern]</b>]:::pattern
            
            subgraph Subsystems ["Internal Subsystems (Facade Hidden)"]
                inv[InventorySystem]:::component
                pay[PaymentSystem]:::component
                ship[ShippingSystem]:::component
            end
            
            factory[OrderFactory<br/><b>[Factory Method Pattern]</b>]:::pattern
            
            subgraph Order_Hierarchy ["Order Class Hierarchy"]
                order[Order (Abstract)]:::component
                std_order[StandardOrder]:::component
                exp_order[ExpressOrder]:::component
            end

            context[OrderContext<br/><b>[State Pattern Context]</b>]:::pattern
            
            subgraph State_Hierarchy ["Order State Hierarchy"]
                state[OrderState (Interface)]:::component
                pending_st[PendingState]:::component
                paid_st[PaidState]:::component
                shipped_st[ShippedState]:::component
            end
            
            collection[OrderCollection<br/><b>[Iterator Pattern]</b>]:::pattern
        end

        subgraph Repository_Persistence_Layer ["Repository & Persistence Layer"]
            db_conn[DatabaseConnection<br/><b>[Singleton Pattern]</b>]:::pattern
        end
    end

    subgraph CSharp_Microservices_Cluster ["Host Windows OS (C# Microservices Cluster)"]
        SSO[Auth SSO Service<br/>Port 5001]:::service
        Search[Search API Service<br/>Port 5002]:::service
        Report[Statistical Report Service<br/>Port 5003]:::service
    end

    subgraph Storage_Tier ["Storage Tier"]
        DB[(SQLite DB<br/>orders.db)]:::db
    end

    %% Interactions
    Client -- "1. HTTP Request" --> api_router
    
    %% Proxy / Gateway Pattern
    api_router -- "HTTP POST (Verify SSO Token)" --> SSO
    api_router -- "HTTP GET (Advanced Search)" --> Search
    api_router -- "HTTP GET (Dynamic Report Summary)" --> Report
    
    %% Controller calling Facade, Iterator, Singleton
    api_router -- "2. place_order()" --> facade
    api_router -- "Traverses / Finds Orders" --> collection
    api_router -- "Reads/Writes User Session" --> db_conn
    
    %% Facade orchestrates subsystems
    facade -- "a. create_order()" --> factory
    factory --> order
    order <|-- std_order
    order <|-- exp_order
    
    facade -- "b. check_stock()" --> inv
    facade -- "c. process_payment()" --> pay
    facade -- "d. arrange_shipping()" --> ship
    
    facade -- "e. proceed() (Updates status)" --> context
    context o-- state
    state <|-- pending_st
    state <|-- paid_st
    state <|-- shipped_st
    
    %% Database Connection (Singleton)
    db_conn -- "Maintains Connection" --> DB
    api_router -- "Fallback Local Database Queries" --> db_conn
    collection -- "Reads records via sqlite3" --> db_conn
```

---

### 2.2 Sơ đồ Class Diagram Tổng thể Hệ thống (Áp dụng 5 Design Patterns)
Sơ đồ thiết kế hoàn thiện biểu diễn cấu trúc của các lớp và mối quan hệ chặt chẽ giữa các thành phần sau khi tích hợp 5 Design Patterns: Singleton, Factory Method, Facade, State và Iterator.

```mermaid
classDiagram
    %% ======= DESIGN PATTERNS ======= %%
    class DatabaseConnection {
        <<Singleton>>
        - _instance : static DatabaseConnection
        - _lock : ThreadLock
        - _db_file : str
        + __new__() : DatabaseConnection
        + _init_db()
        + query(sql : str, params : tuple) : list
        + execute(sql : str, params : tuple) : int
    }

    class OrderFactory {
        <<Factory Method>>
        + create_order(productId : int, type : str) : Order
    }

    class OrderFacade {
        <<Facade>>
        - inventorySystem : InventorySystem
        - paymentSystem : PaymentSystem
        - shippingSystem : ShippingSystem
        + place_order(productId : int, type : str, address : str) : dict
    }

    class OrderState {
        <<State - Interface>>
        + next_step(context : OrderContext)* str
        + get_status_name()* str
    }

    class OrderContext {
        <<State Context>>
        - state : OrderState
        + __init__()
        + set_state(state : OrderState)
        + proceed() : str
        + current_status() : str
    }

    class OrderCollection {
        <<Iterator>>
        - _orders : list
        - _index : int
        + add_order(order_data : dict)
        + __iter__() : OrderCollection
        + __next__() : dict
        + find_order(order_id : int) : dict
    }

    %% ======= CLASSES & MODELS ======= %%
    class OrderController {
        + login()
        + get_users()
        + place_order()
        + search_order()
    }
    
    class Order {
        <<Abstract Model>>
        + product_id : int
        + get_shipping_cost()* float
        + get_order_type()* str
    }
    class StandardOrder {
        + get_shipping_cost() float ($2.5)
        + get_order_type() str ("Standard")
    }
    class ExpressOrder {
        + get_shipping_cost() float ($15.0)
        + get_order_type() str ("Express")
    }

    class InventorySystem {
        + check_stock(product_id : int) bool
    }
    class PaymentSystem {
        + process_payment(amount : float) bool
    }
    class ShippingSystem {
        + arrange_shipping(product_id : int, address : str) str
    }
    
    Order <|-- StandardOrder
    Order <|-- ExpressOrder

    OrderState <|-- PendingState
    OrderState <|-- PaidState
    OrderState <|-- ShippedState

    %% ======= MỐI QUAN HỆ ======= %%
    OrderController --> OrderFacade : uses
    OrderController --> OrderCollection : iterates
    OrderController --> DatabaseConnection : accesses
    OrderFacade --> OrderFactory : instantiates Orders
    OrderFacade --> OrderContext : runs State Machine
    OrderFacade --> InventorySystem : delegates
    OrderFacade --> PaymentSystem : delegates
    OrderFacade --> ShippingSystem : delegates
    OrderFactory ..> Order : creates
    OrderContext o--> OrderState : delegates behavior
```

---

### 2.3 Sơ đồ Chi tiết Mẫu thiết kế State (Trước khi áp dụng - Before)
Khi chưa có State Pattern, logic cập nhật và quản lý trạng thái của Đơn hàng gặp lỗi **Tight Coupling** và vi phạm nguyên lý **Open/Closed Principle (OCP)** của SOLID. Các trạng thái được kiểm soát thông qua biến chuỗi/mã trạng thái (`status: string`) và một chuỗi các câu lệnh `if/else` rẽ nhánh lồng nhau phức tạp bên trong một lớp xử lý nghiệp vụ monolithic (`OrderService`).

```mermaid
classDiagram
    class OrderController {
        +place_order(product_id: int, type: string, address: string)
        +update_order_status(order_id: int, target_status: string)
    }
    
    class Order {
        +id: int
        +product_id: int
        +type: string
        +status: string
        +shipping_cost: float
        +address: string
        +tracking_code: string
    }

    class OrderService_Monolithic {
        -db_connection: DatabaseConnection
        +create_order(product_id: int, type: string, address: string): Order
        +process_payment(order_id: int): bool
        +arrange_shipping(order_id: int): string
        +update_status(order_id: int, target_status: string): string
    }

    note for OrderService_Monolithic "Logic update_status() phụ thuộc vào if/else lồng nhau:\n\nif self.status == 'Pending':\n    if target_status == 'Paid':\n        self.status = 'Paid'\n        # Ghi SQLite...\n    else:\n        raise Exception('Trạng thái không hợp lệ')\nelif self.status == 'Paid':\n    if target_status == 'Shipped':\n        self.status = 'Shipped'\n        # Ghi SQLite...\n    else:\n        raise Exception('Trạng thái không hợp lệ')\nelif self.status == 'Shipped':\n    raise Exception('Không thể chuyển trạng thái thêm')"

    OrderController --> OrderService_Monolithic : Gọi nghiệp vụ đặt & cập nhật
    OrderService_Monolithic ..> Order : Tạo & trực tiếp thay đổi thuộc tính
```

**Nhược điểm của thiết kế cũ:**
1. **Spaghetti Code**: Mã nguồn bị phình to khi thêm trạng thái mới (ví dụ: `Cancelled`, `Refunded`, `Delivered`). Lớp `OrderService` trở thành God Class gánh vác mọi logic chuyển đổi.
2. **Dễ phát sinh lỗi**: Việc trực tiếp thay đổi thuộc tính `status` ở nhiều nơi làm mất đi tính đóng gói dữ liệu, dễ dẫn đến trạng thái đơn hàng bị cập nhật sai luồng logic nghiệp vụ.

---

### 2.4 Sơ đồ Chi tiết Mẫu thiết kế State (Sau khi áp dụng - After)
Sau khi áp dụng mẫu thiết kế **State (Behavioral Group)**, mỗi trạng thái của đơn hàng được đóng gói thành một lớp thực thể riêng biệt triển khai từ giao diện `OrderState`. Toàn bộ logic kiểm soát luồng di chuyển trạng thái được phân bổ về từng Class trạng thái cụ thể, loại bỏ hoàn toàn các câu lệnh `if/else` lồng nhau.

```mermaid
classDiagram
    class OrderFacade {
        -inventory: InventorySystem
        -payment: PaymentSystem
        -shipping: ShippingSystem
        +place_order(product_id: int, order_type: string, address: string): dict
    }

    class OrderContext {
        -state: OrderState
        +__init__()
        +set_state(state: OrderState)
        +proceed(): string
        +current_status(): string
    }

    class OrderState {
        <<interface>>
        +next_step(context: OrderContext)* string
        +get_status_name()* string
    }

    class PendingState {
        +next_step(context: OrderContext) string
        +get_status_name() string
    }

    class PaidState {
        +next_step(context: OrderContext) string
        +get_status_name() string
    }

    class ShippedState {
        +next_step(context: OrderContext) string
        +get_status_name() string
    }

    OrderFacade --> OrderContext : Điều phối quy trình và vòng đời đơn hàng
    OrderContext o--> OrderState : Tập hợp trạng thái hiện tại (Aggregation)
    OrderState <|.. PendingState : Triển khai (Realization)
    OrderState <|.. PaidState : Triển khai (Realization)
    OrderState <|.. ShippedState : Triển khai (Realization)

    note for PendingState "next_step(context):\n    context.set_state(PaidState())\n    return 'Pending -> Paid'"
    note for PaidState "next_step(context):\n    context.set_state(ShippedState())\n    return 'Paid -> Shipped'"
    note for ShippedState "next_step(context):\n    return 'Đã giao vận chuyển (Trạng thái cuối)'"
```

**Ưu điểm vượt trội của thiết kế mới:**
1. **Loose Coupling & Single Responsibility**: Tách biệt rõ ràng. `PendingState` chỉ quản lý việc chuyển sang `PaidState`, `PaidState` chỉ quản lý chuyển sang `ShippedState`.
2. **Dễ bảo trì và mở rộng (OCP)**: Khi hệ thống cần thêm trạng thái `CancelledState`, ta chỉ cần tạo một Class mới kế thừa từ `OrderState` và thay đổi liên kết chuyển tiếp từ `PendingState` hoặc `PaidState` mà không cần đụng tới code hiện tại của các trạng thái khác.
3. **Mã nguồn sạch sẽ**: Loại bỏ hoàn toàn khối `if-else` lồng nhau. Việc quản lý chuyển dịch trạng thái thông qua cơ chế đa hình (`Polymorphism`) thay vì kiểm tra giá trị chuỗi thủ công.

---

### 2.5 Sơ đồ Sequence Diagram: Luồng nghiệp vụ
So sánh sự khác biệt lớn về độ phức tạp khi có và không có các mẫu thiết kế:

#### A. Khi chưa có Facade và State Pattern
Client hoặc Controller phải liên hệ và kiểm tra thủ công với từng Subsystem độc lập, sau đó sử dụng các logic rẻ nhánh `if/else` để đổi trạng thái đơn hàng.

```mermaid
sequenceDiagram
    participant C as Controller / Client
    participant S as OrderService
    participant DB as System DB

    C->>S: create_order(prod_id, type)
    S->>S: if Inventory.check() == True
    S->>S: if Payment.pay() == True
    S->>DB: Save Order (status="Pending")
    
    C->>S: upgrade_status(orderId, "Paid")
    S->>S: if current_status == "Pending"
    S->>DB: Update (status="Paid")
```

#### B. Khi có Facade và State Pattern
Controller giao tiếp ở mức độ trừu tượng cao nhất. `OrderFacade` tự động điều phối các Subsystem ngầm bên dưới, và trạng thái đơn hàng được luân chuyển tuần tự tự động qua `OrderContext`.

```mermaid
sequenceDiagram
    participant C as OrderController
    participant F as OrderFacade (Structural)
    participant ST as OrderContext (Behavioral)
    
    C->>F: place_order(product_id, type, address)
    
    F->>F: inventory.check()
    F->>F: payment.process()
    
    F->>ST: new OrderContext()
    note over ST: Trạng thái bắt đầu: PendingState

    F->>ST: proceed()
    note over ST: PendingState nâng cấp Context lên PaidState
    
    F->>ST: proceed()
    note over ST: PaidState nâng cấp Context lên ShippedState
    
    F-->>C: Trả kết quả {status: Success, final_state: Shipped}
```

#### C. Sơ đồ tương tác chéo giữa Python Web MVC và các C# Microservices (Xác thực & Báo cáo)

Để đạt được mô hình kiến trúc phân tán thực tế, Web Component gọi HTTP REST tới các C# Microservices độc lập. Dưới đây là luồng tương tác thực tế bao gồm cơ chế Fallback (dự phòng) tự động khi các service C# ở trạng thái offline.

**1. Luồng Xác thực người dùng (SSO Service - Port 5001)**

```mermaid
sequenceDiagram
    autonumber
    actor User as Client (Web Frontend)
    participant Web as Python FastAPI (Web MVC)
    participant CSharpSSO as C# SSOService (:5001)
    participant DB as SQLite Database (Local)

    User->>Web: POST /api/auth/login {username, password}
    Web->>CSharpSSO: HTTP POST /api/sso/login {username, password}
    alt C# SSOService Online
        CSharpSSO-->>Web: Trả về 200 OK & JWT Token + User info
        Web-->>User: Đăng nhập thành công (Nguồn: C# SSO Microservice)
    else C# SSOService Offline / Lỗi (Fallback)
        Web->>Web: Ghi nhận cảnh báo & chuyển sang Fallback
        Web->>DB: SELECT * FROM users WHERE username=? AND password=?
        alt User hợp lệ trong SQLite
            DB-->>Web: Trả về thông tin User
            Web-->>User: Đăng nhập thành công (Nguồn: SQLite Local Fallback)
        else User không tồn tại / Sai pass
            DB-->>Web: Không tìm thấy
            Web-->>User: Trả về lỗi 401/error
        end
    end
```

**2. Luồng Lấy dữ liệu Báo cáo (Report Service - Port 5003)**

```mermaid
sequenceDiagram
    autonumber
    actor User as Client (Web Frontend)
    participant Web as Python FastAPI (Web MVC)
    participant CSharpReport as C# ReportService (:5003)

    User->>Web: GET /api/report/csharp-summary
    Web->>CSharpReport: HTTP GET /api/report/summary
    alt C# ReportService Online
        CSharpReport-->>Web: Trả về 200 OK (total_orders, total_revenue)
        Web-->>User: Trả về dữ liệu thống kê thật (Nguồn: C# Report Microservice)
    else C# ReportService Offline (Fallback)
        Web->>Web: Bắt ngoại lệ & kích hoạt Mock Fallback
        Web-->>User: Trả về dữ liệu giả lập dự phòng (Nguồn: SQLite Local Cache Fallback)
    end
```

---

## PHẦN 3: PHÂN TÍCH CHI TIẾT 5 DESIGN PATTERNS ÁP DỤNG

Dưới đây là chi tiết các file cài đặt 5 Design Patterns trong thư mục [Project/src/web_mvc/app/patterns/](file:///d:/HSU/2533Semester%203(2025-2026)/Ki%E1%BA%BFn%20tr%C3%BAc%20ph%E1%BA%A7n%20m%E1%BB%81m/Kien_Truc_Phan_Mem_Test-main/Kien_Truc_Phan_Mem_Test-main/Project/src/web_mvc/app/patterns):

### 3.1 Singleton Pattern (`singleton.py`)
*   **Mục đích**: Đảm bảo chỉ có duy nhất một kết nối Database Connection được duy trì trong suốt thời gian ứng dụng chạy để thực thi truy vấn tới SQLite.
*   **Mã nguồn**:
```python
import sqlite3
import threading
import logging

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()
    _db_file = "orders.db"

    def __new__(cls):
        # Double-Checked Locking (Đảm bảo an toàn luồng)
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    logging.info("Khởi tạo instance DatabaseConnection (Singleton) lần đầu...")
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        # Tạo bảng và nạp dữ liệu mẫu
        ...
```
*   **Lợi ích**: Ngăn chặn tình trạng tạo quá nhiều kết nối gây cạn kiệt tài nguyên hệ thống, chống Race Condition khi có hàng trăm request gọi API đồng thời nhờ cơ chế khóa Lock bảo vệ.

---

### 3.2 Factory Method Pattern (`factory.py`)
*   **Mục đích**: Tách biệt logic khởi tạo đối tượng Đơn hàng khỏi mã nguồn gọi nó. Tự động trả về đúng kiểu đơn hàng (`StandardOrder` hoặc `ExpressOrder`) dựa trên tham số vận chuyển.
*   **Mã nguồn**:
```python
from abc import ABC, abstractmethod

class Order(ABC):
    def __init__(self, product_id: int):
        self.product_id = product_id

    @abstractmethod
    def get_shipping_cost(self) -> float: pass

class StandardOrder(Order):
    def get_shipping_cost(self) -> float: return 2.5

class ExpressOrder(Order):
    def get_shipping_cost(self) -> float: return 15.0

class OrderFactory:
    @staticmethod
    def create_order(product_id: int, order_type: str) -> Order:
        if order_type.lower() == 'express':
            return ExpressOrder(product_id)
        return StandardOrder(product_id)
```
*   **Lợi ích**: Tăng tính mở rộng. Khi doanh nghiệp mở thêm các dịch vụ vận chuyển mới (như vận chuyển máy bay, hoả tốc 2h), ta chỉ cần tạo thêm Class kế thừa từ `Order` mà không cần thay đổi bất kỳ dòng code nào ở tầng Controller.

---

### 3.3 Facade Pattern (`facade.py`)
*   **Mục đích**: Cung cấp một giao diện (Interface) đơn giản cho Controller gọi, che giấu đi sự tương tác phức tạp của 3 subsystem (Inventory, Payment, Shipping).
*   **Mã nguồn**:
```python
class OrderFacade:
    def __init__(self):
        self.inventory = InventorySystem()
        self.payment = PaymentSystem()
        self.shipping = ShippingSystem()

    def place_order(self, product_id: int, order_type: str, address: str) -> dict:
        # Tự động kết hợp 3 subsystem + Factory + State máy trạng thái
        order = OrderFactory.create_order(product_id, order_type)
        order_process = OrderContext()
        
        self.inventory.check_stock(product_id)
        self.payment.process_payment(order.get_shipping_cost())
        order_process.proceed() # Pending -> Paid
        
        tracking_code = self.shipping.arrange_shipping(product_id, address)
        order_process.proceed() # Paid -> Shipped
        
        return {
            "status": "Success",
            "order_type": order.get_order_type(),
            "final_state": order_process.current_status(),
            "tracking_code": tracking_code
        }
```
*   **Lợi ích**: Giảm sự phụ thuộc chéo (coupling) giữa hệ thống bên ngoài và các class nội bộ. Controller chỉ cần gọi đúng một hàm duy nhất để hoàn thành chuỗi đặt hàng phức tạp.

---

### 3.4 State Pattern (`state.py`)
*   **Mục đích**: Đóng gói trạng thái của Đơn hàng thành các đối tượng độc lập. Mỗi đối tượng tự quyết định logic chuyển dịch trạng thái tiếp theo mà không cần dùng câu lệnh rẽ nhánh `if/else`.
*   **Mã nguồn**:
```python
class OrderState(ABC):
    @abstractmethod
    def next_step(self, context) -> str: pass

class PendingState(OrderState):
    def next_step(self, context) -> str:
        context.set_state(PaidState())
        return "Pending -> Paid"

class PaidState(OrderState):
    def next_step(self, context) -> str:
        context.set_state(ShippedState())
        return "Paid -> Shipped"

class OrderContext:
    def __init__(self):
        self.state = PendingState()
    # Các hàm proceed(), set_state(), current_status()
    ...
```
*   **Lợi ích**: Mã nguồn cực kỳ gọn gàng. Khi quy trình đơn hàng bổ sung thêm các trạng thái mới (như Trả hàng, Giao thất bại), ta chỉ cần viết thêm Class trạng thái mới và trỏ luồng dịch chuyển mà không cần chỉnh sửa các hàm logic nghiệp vụ hiện hữu.

---

### 3.5 Iterator Pattern (`iterator.py`)
*   **Mục đích**: Cho phép duyệt qua danh sách các đơn hàng và tìm kiếm đơn hàng mà không để lộ cấu trúc dữ liệu lưu trữ bên trong (ở đây là mảng `_orders`).
*   **Mã nguồn**:
```python
class OrderCollection:
    def __init__(self):
        self._orders = []

    def add_order(self, order_data: dict):
        self._orders.append(order_data)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._orders):
            result = self._orders[self._index]
            self._index += 1
            return result
        raise StopIteration

    def find_order(self, order_id: int):
        for order in self:
            if order.get("id") == order_id:
                return order
        return None
```
*   **Lợi ích**: Khách hàng (Controller) có thể sử dụng vòng lặp `for...in` để duyệt danh sách đơn hàng bình thường. Nếu sau này cấu trúc dữ liệu lưu trữ thay đổi từ mảng sang cấu trúc Tree hoặc Hash, mã nguồn bên ngoài vẫn giữ nguyên không thay đổi.

---

## PHẦN 4: HƯỚNG DẪN TRIỂN KHAI & VẬN HÀNH (RUN GUIDE)

### 4.1 Khởi chạy Web Component (Python FastAPI + Giao diện)
Bạn có thể chọn một trong hai phương án dưới đây tùy thuộc vào môi trường máy:

#### 👉 Phương án A: Khởi chạy nhanh bằng Docker (Khuyên dùng)
Nếu máy tính của bạn đã cài đặt Docker Desktop:
1.  Mở PowerShell/Terminal tại thư mục dự án Web:
    ```powershell
    cd "D:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Project\src\web_mvc"
    ```
2.  Khởi chạy Container:
    ```powershell
    docker-compose up -d --build
    ```
3.  **Trải nghiệm**:
    *   Truy cập giao diện Web tại: `http://localhost:8000`
    *   Xem tài liệu API tại: `http://localhost:8000/docs`

#### 👉 Phương án B: Khởi chạy thủ công bằng Python local
Nếu máy tính của bạn đã cài đặt Python 3.10+:
1.  Di chuyển vào thư mục Web và tạo môi trường ảo Python:
    ```powershell
    cd "D:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Project\src\web_mvc"
    python -m venv venv
    ```
2.  Kích hoạt môi trường ảo:
    *   *Windows (PowerShell)*: `.\venv\Scripts\activate`
    *   *macOS/Linux*: `source venv/bin/activate`
3.  Cài đặt các thư viện và chạy:
    ```powershell
    pip install -r requirements.txt
    python main.py
    ```

---

### 4.2 Khởi chạy cụm C# Microservices (.NET 8.0)
Cụm Microservices độc lập viết bằng C# chạy trên 3 cổng khác nhau: SSO (5001), Search (5002), và Report (5003).

#### Hướng dẫn chạy nhanh bằng Script tự động:
1.  Mở một cửa sổ PowerShell mới (quyền Administrator).
2.  Di chuyển vào thư mục chứa Microservices:
    ```powershell
    cd "D:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Project\src\microservices_csharp"
    ```
3.  Chạy script khởi động:
    ```powershell
    powershell -ExecutionPolicy Bypass -File .\run_microservices.ps1
    ```
    *(Hệ thống sẽ tự động bật 3 cửa sổ CMD chạy độc lập 3 dịch vụ).*

#### Các đường dẫn kiểm thử API (REST JSON):
*   **SSO Service API**: [Xác thực Token](http://localhost:5001/api/sso/verify?token=sso_token_secure_admin_xyz)
*   **Search Service API**: [Tìm kiếm đơn hàng 101](http://localhost:5002/api/search/orders/101)
*   **Report Service API**: [Xem báo cáo doanh thu](http://localhost:5003/api/report/summary)

---

### 4.3 Cách tắt hệ thống
*   **Web Docker**: Chạy lệnh `docker-compose down` tại thư mục `Project/src/web_mvc`.
*   **Web Python local**: Nhấn `Ctrl + C` tại cửa sổ CMD đang chạy server.
*   **C# Microservices**: Tắt 3 cửa sổ Console CMD mới được mở ra trong quá trình chạy script.

---

## PHẦN 5: KỊCH BẢN NỘI DUNG 13 SLIDE THUYẾT TRÌNH BẢO VỆ

*Các slide được biên soạn theo trình tự thuyết trình khoa học giúp sinh viên dễ dàng chuẩn bị.*

*   **Slide 1: Trang tiêu đề & Thành viên nhóm**
    *   *Nội dung*: Hệ thống Quản lý Đơn hàng (OMS) ứng dụng kiến trúc n-Tier & C# Microservices kết hợp áp dụng 5 Design Patterns.
    *   *Kịch bản nói*: Kính chào hội đồng phản biện, hôm nay nhóm chúng em xin trình bày về đề tài xây dựng hệ thống OMS đáp ứng tính linh hoạt và mở rộng cao...
*   **Slide 2: Bài toán thực tế & Thách thức**
    *   *Nội dung*: Spaghetti code khi quy trình xử lý đơn hàng phức tạp. Khó khăn khi đổi trạng thái đơn hàng nếu dùng lệnh `if/else` lồng nhau.
    *   *Kịch bản nói*: Trong thực tế, quy trình đơn hàng tương tác với rất nhiều hệ thống con. Nếu code theo kiểu truyền thống, mã nguồn sẽ trở nên cực kỳ rối ren và dễ phát sinh lỗi...
*   **Slide 3: Giải pháp kiến trúc tổng thể**
    *   *Nội dung*: Gồm Web Component (Python FastAPI MVC + SQLite) và cụm 3 C# Microservices (SSO, Search, Report).
    *   *Kịch bản nói*: Để giải quyết vấn đề, chúng em tách biệt làm 2 khối: Khối Web chính viết bằng FastAPI, và cụm 3 Microservices viết bằng C# để xử lý các tác vụ phụ...
*   **Slide 4: Singleton Pattern (Creational Group)**
    *   *Nội dung*: Class `DatabaseConnection` kết nối SQLite `orders.db`. Đảm bảo an toàn đa luồng (Thread-safe Lock).
    *   *Kịch bản nói*: Chúng em áp dụng Singleton cho kết nối DB để tiết kiệm tài nguyên và chống Race Condition khi có nhiều người truy cập...
*   **Slide 5: Factory Method Pattern (Creational Group)**
    *   *Nội dung*: Lớp cha `Order`, các lớp con `StandardOrder` và `ExpressOrder`. `OrderFactory` khởi tạo.
    *   *Kịch bản nói*: Nhóm sử dụng Factory Method để tách biệt quá trình tạo đơn hàng thường hoặc hoả tốc, giúp dễ dàng thêm các loại giao hàng mới sau này...
*   **Slide 6: Facade Pattern (Structural Group)**
    *   *Nội dung*: Lớp `OrderFacade` che giấu sự phức tạp của 3 subsystem: Inventory, Payment và Shipping.
    *   *Kịch bản nói*: Tầng Controller sẽ không làm việc trực tiếp với Kho hay Thanh toán, mà thông qua Facade giúp code của Controller cực kỳ sạch sẽ và sáng sủa...
*   **Slide 7: State Pattern (Behavioral Group)**
    *   *Nội dung*: `OrderContext`, các lớp trạng thái `PendingState`, `PaidState`, `ShippedState`.
    *   *Kịch bản nói*: Thay vì dùng if-else cập nhật trạng thái đơn hàng, mỗi trạng thái được đóng gói thành một lớp riêng và tự chuyển đổi luân phiên tự động...
*   **Slide 8: Iterator Pattern (Behavioral Group)**
    *   *Nội dung*: Lớp `OrderCollection` triển khai `__iter__` và `__next__`. Duyệt và tìm kiếm đơn hàng.
    *   *Kịch bản nói*: Iterator Pattern giúp chúng em duyệt qua các đơn hàng lấy lên từ SQLite mà không để lộ cấu trúc lưu trữ nội bộ của danh sách...
*   **Slide 9: Sơ đồ Sequence Diagram (So sánh trước & sau có Pattern)**
    *   *Nội dung*: Minh hoạ luồng gọi hàm phức tạp trước đây so với sự tinh giản, trừu tượng hóa cao khi áp dụng Facade + State Pattern.
    *   *Kịch bản nói*: Nhìn vào sơ đồ Sequence này, quý thầy cô có thể thấy sự cải tiến vượt bậc. Controller nay chỉ cần gọi một hàm của Facade, và trạng thái tự chuyển đổi...
*   **Slide 10: Minh hoạ cơ sở dữ liệu thật (SQLite)**
    *   *Nội dung*: Mô tả cấu trúc bảng `users` và `orders` được lưu trữ bền vững tại file `orders.db`.
    *   *Kịch bản nói*: Toàn bộ dữ liệu của dự án đã được tích hợp SQLite thật qua cơ chế Singleton, đảm bảo dữ liệu được lưu trữ vĩnh viễn thay vì mất đi khi tắt RAM...
*   **Slide 11: Demo Giao diện Web Frontend (View)**
    *   *Nội dung*: Giao diện Dark Mode đẹp mắt, các chức năng Đăng nhập, CRUD Users, Đặt hàng và Tra cứu.
    *   *Kịch bản nói*: Đây là giao diện ứng dụng OMS của chúng em. Người dùng có thể thực hiện đăng ký tài khoản, đăng nhập, đặt đơn hàng hoả tốc và theo dõi đơn hàng thời gian thực...
*   **Slide 12: Trình diễn cụm C# Microservices**
    *   *Nội dung*: Khởi chạy 3 Microservices C# (SSO, Search, Report) và kết quả phản hồi REST API.
    *   *Kịch bản nói*: Cụm Microservice C# của chúng em được viết tinh gọn, chạy ổn định song song trên các cổng 5001, 5002, 5003 để bổ trợ cho Web chính...
*   **Slide 13: Kết luận & Giá trị cốt lõi**
    *   *Nội dung*: Mã nguồn đạt chuẩn SOLID, Loose Coupling, dễ bảo trì và khả năng mở rộng cao.
    *   *Kịch bản nói*: Tóm lại, hệ thống OMS của chúng em đã áp dụng thành công các nguyên lý kiến trúc tiên tiến. Nhóm chúng em xin chân thành cảm ơn hội đồng và sẵn sàng nhận câu hỏi...

---

## PHẦN 6: BỘ CÂU HỎI PHẢN BIỆN BẢO VỆ GỢI Ý (Q&A)

### ❓ Câu 1: Tại sao em lại chọn SQLite cho dự án này mà không phải SQL Server hay MySQL?
*   **Trả lời**: Dạ, SQLite là hệ quản trị cơ sở dữ liệu dạng file gọn nhẹ, không yêu cầu cài đặt dịch vụ ngầm phức tạp, rất phù hợp cho mục tiêu trình diễn các mẫu thiết kế và kiến trúc của bài tập lớn. Tuy nhiên, nhờ áp dụng **Singleton Pattern** cho kết nối database và mô hình phân tầng **Repository**, nếu dự án cần nâng cấp lên MySQL hay SQL Server trong tương lai, chúng em chỉ cần sửa đổi chuỗi kết nối trong file Singleton mà không cần chỉnh sửa bất kỳ dòng code nào ở tầng Controller hay View.

### ❓ Câu 2: Trong lớp `DatabaseConnection` (Singleton), làm sao em đảm bảo tính an toàn đa luồng (Thread-safe)?
*   **Trả lời**: Dạ, trong môi trường Web API, nhiều request của người dùng có thể gửi tới đồng thời (Multi-threading). Để tránh tình trạng tạo ra nhiều thực thể kết nối cùng lúc (Race Condition), chúng em đã áp dụng kỹ thuật **Double-Checked Locking** kết hợp thuộc tính `_lock = threading.Lock()`. Khi khởi tạo, hệ thống sẽ kiểm tra thực thể 2 lần trước và sau khi chiếm giữ khóa Lock để đảm bảo an toàn tuyệt đối.

### ❓ Câu 3: Điểm khác biệt lớn nhất khi em áp dụng State Pattern so với dùng `if/else` thông thường là gì?
*   **Trả lời**: Dạ, nếu dùng `if/else` thông thường, mỗi khi thay đổi trạng thái đơn hàng, chúng ta phải viết hàng loạt câu điều kiện lồng nhau trong một phương thức duy nhất của lớp `OrderService`, làm cho lớp này phình to và rất khó đọc (Spaghetti Code). Với State Pattern, mỗi trạng thái (Pending, Paid, Shipped) là một lớp độc lập, chịu trách nhiệm tự xử lý logic của chính nó và tự động chuyển sang trạng thái kế tiếp. Điều này giúp mã nguồn tuân thủ nguyên lý **Single Responsibility** (Đơn nhiệm) và **Open/Closed** (Mở rộng nhưng đóng đóng với sửa đổi) của nguyên lý SOLID.

### ❓ Câu 4: Facade Pattern có vai trò gì trong quy trình Đặt hàng (Place Order) của hệ thống?
*   **Trả lời**: Quy trình đặt đơn hàng liên kết nhiều hành động phức tạp: kiểm kho (`InventorySystem`), thanh toán tiền (`PaymentSystem`), và giao vận (`ShippingSystem`). Nếu Controller gọi trực tiếp cả 3 lớp này thì Controller sẽ bị phụ thuộc chặt chẽ (Tight Coupling). Chúng em sử dụng `OrderFacade` để làm trung gian điều phối tất cả các hệ thống này. Controller chỉ cần gọi đúng một phương thức `place_order` của Facade là xong, giúp mã nguồn ở tầng Controller tối giản và độc lập.

---

## PHẦN 7: TÀI LIỆU API ĐẦY ĐỦ CHI TIẾT (API DOCUMENTATION)

### 7.1 WEB API COMPONENT (Python FastAPI - Cổng 8000)

*   **Đăng nhập (Login)**:
    *   *Endpoint*: `POST /api/auth/login`
    *   *Request Body*: `{"username": "admin", "password": "123"}`
    *   *Response (200 OK)*: `{"message": "Đăng nhập thành công!", "token": "fake_jwt_1", "user": {"id": 1, "username": "admin", "email": "admin@example.com", "is_admin": true}}`

*   **Xem danh sách người dùng**:
    *   *Endpoint*: `GET /api/users`
    *   *Response (200 OK)*: Danh sách người dùng trong SQLite.

*   **Đăng ký tài khoản mới**:
    *   *Endpoint*: `POST /api/users`
    *   *Request Body*: `{"username": "customer", "password": "123", "email": "customer@example.com"}`
    *   *Response (200 OK)*: `{"message": "Đăng ký thành công User ID 3!"}`

*   **Đặt hàng (Facade)**:
    *   *Endpoint*: `POST /api/orders/place`
    *   *Request Body*: `{"product_id": 1, "order_type": "express", "address": "TPHCM"}`
    *   *Response (200 OK)*: `{"status": "Success", "order_type": "Express", "final_state": "Shipped", "tracking_code": "...", "order_id": 103}`

*   **Tìm kiếm đơn hàng (Iterator)**:
    *   *Endpoint*: `GET /api/orders/search/{order_id}`
    *   *Response (200 OK)*: Dữ liệu đơn hàng chi tiết hoặc thông báo lỗi `{"error": "..."}`.

*   **Xem tất cả đơn hàng (Iterator)**:
    *   *Endpoint*: `GET /api/orders/`
    *   *Response (200 OK)*: Mảng JSON toàn bộ đơn hàng trong SQLite.

### 7.2 MICROSERVICES COMPONENT (C# .NET - Cổng 5001, 5002, 5003)

*   **SSO Service**:
    *   *Xác thực Token*: `GET http://localhost:5001/api/sso/verify?token=sso_token_secure_admin_xyz`
    *   *Response (200 OK)*: `{"valid": true, "user": "admin", "source": "SSO C# Microservice"}`
*   **Search Service**:
    *   *Tìm nâng cao*: `GET http://localhost:5002/api/search/orders/{order_id}`
    *   *Response (200 OK)*: Đơn hàng nâng cao dạng JSON kèm trường `searched_at`.
*   **Report Service**:
    *   *Báo cáo thống kê*: `GET http://localhost:5003/api/report/summary`
    *   *Response (200 OK)*: `{ "total_orders": 52, "total_revenue": 12450.5, "shipping_summary": [...] }`

---

## PHẦN 8: HƯỚNG DẪN SỬA LỖI VÀ XỬ LÝ SỰ CỐ (TROUBLESHOOTING GUIDE)

### 8.1 Lỗi chạy Script PowerShell (.ps1)
*   *Lỗi*: Script is disabled on this system.
*   *Cách sửa*: Chạy lệnh PowerShell:
    ```powershell
    powershell -ExecutionPolicy Bypass -File .\run_microservices.ps1
    ```
    Hoặc mở PowerShell quyền Admin và gõ: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine`.

### 8.2 Lỗi xung đột cổng chạy (Address already in use)
*   *Lỗi*: Cổng 8000, 5001, 5002 hoặc 5003 đã bị chiếm dụng.
*   *Cách sửa*: Tìm PID bằng lệnh: `netstat -ano | findstr :8000` (giả sử cổng 8000), sau đó tắt bằng lệnh: `taskkill /F /PID <PID_số>`.

### 8.3 Lỗi Docker Engine chưa chạy
*   *Lỗi*: Cannot connect to the Docker daemon.
*   *Cách sửa*: Hãy khởi chạy phần mềm **Docker Desktop** trên máy tính Windows của bạn và đợi cho biểu tượng chú cá voi chuyển sang màu xanh lá trước khi chạy docker-compose.

### 8.4 Lỗi SQLite database bị khóa (Database is locked)
*   *Lỗi*: sqlite3.OperationalError: database is locked.
*   *Cách sửa*: Tắt các ứng dụng xem DB bên ngoài (như DB Browser for SQLite) đang mở tệp `orders.db` ở chế độ ghi, sau đó khởi động lại server API.

---

## PHẦN 9: KỊCH BẢN DEMO BẢO VỆ DỰ ÁN CHI TIẾT (DEMO GUIDE)

### 9.1 Lệnh chạy dự án nhanh nhất
*   **Chạy Web FastAPI + SQLite (Docker)**:
    ```powershell
    cd "D:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Project\src\web_mvc"
    docker-compose up -d --build
    ```
*   **Chạy 3 C# Microservices (PowerShell script)**:
    ```powershell
    cd "D:\HSU\2533Semester 3(2025-2026)\Kiến trúc phần mềm\Kien_Truc_Phan_Mem_Test-main\Kien_Truc_Phan_Mem_Test-main\Project\src\microservices_csharp"
    powershell -ExecutionPolicy Bypass -File .\run_microservices.ps1
    ```

### 9.2 Kịch bản các bước Demo trên giao diện (http://localhost:8000)

#### 📍 Bước 1: Giới thiệu giao diện & Kết nối DB Singleton
*   **Thao tác**: Cuộn trang web, chỉ vào header của Dashboard hiển thị `SQLite Connected (Singleton)`.
*   **Lời thoại**: *"Đây là giao diện chính của Hệ thống Quản lý Đơn hàng (OMS). Ở góc bên phải tiêu đề, hệ thống hiển thị trạng thái kết nối Database được thiết lập thông qua Singleton Pattern để đảm bảo ứng dụng dùng duy nhất một Instance kết nối SQLite trong suốt vòng đời chạy."*

#### 📍 Bước 2: Đăng ký & Đăng nhập tài khoản cục bộ (Local Fallback)
*   **Thao tác**: Nhấn Đăng xuất, sang tab Đăng ký tạo tài khoản `customer_test`/`123`, sau đó sang tab Đăng nhập để truy cập.
*   **Lời thoại**: *"Khi các C# Microservices chưa online, hệ thống tự động chuyển hướng xác thực xuống database SQLite cục bộ. Giao diện hiển thị rõ nguồn xác thực là SQLite Local Database Fallback."*

#### 📍 Bước 3: Xem danh sách thành viên (User Management)
*   **Thao tác**: Nhấp tab **Quản lý Users** trên Sidebar bên trái, chỉ ra tài khoản `customer_test` vừa tạo nằm ở cuối bảng.
*   **Lời thoại**: *"Dữ liệu tài khoản mới đăng ký đã được ghi nhận thành công và hiển thị thời gian thực từ database SQLite."*

#### 📍 Bước 4: Tạo đơn hàng mới (Facade + Factory + State Pattern)
*   **Thao tác**: Vào tab **Đặt hàng & Tra cứu**, chọn sản phẩm (iPhone), chọn giao hàng hỏa tốc (Express - ship $15.0), nhập địa chỉ, nhấn Đặt hàng.
*   **Lời thoại**: *"Khi click Đặt hàng, Facade Pattern điều phối Kho, Thanh toán và Vận chuyển ngầm; Factory Method khởi tạo Class ExpressOrder để tính phí ship $15.0; và State Pattern quản lý vòng đời trạng thái đơn hàng (Pending -> Paid -> Shipped) tự động."*

#### 📍 Bước 5: Tra cứu đơn hàng (Proxy C# Search & Fallback Iterator)
*   **Thao tác**:
    *   *C# Search Service Online*: Tìm ID `101` hoặc `102` -> Nhãn hiển thị **"Nguồn tìm kiếm: C# Search Microservice (:5002)"**.
    *   *C# Search Service Offline*: Tìm ID `106` (đơn hàng vừa tạo) -> Nhãn hiển thị **"Nguồn tìm kiếm: SQLite Local (Iterator Pattern Fallback)"**.
*   **Lời thoại**: *"Tìm kiếm đơn hàng ưu tiên Proxy gọi C# Search Service cổng 5002. Nếu service offline, hệ thống tự động fallback sử dụng Iterator Pattern duyệt tìm trong database SQLite cục bộ."*

#### 📍 Bước 6: Demo liên thông dữ liệu chéo (SSO & Report)
*   **Thao tác**: Đăng nhập tài khoản `admin`/`123`. Lúc này nhãn đổi thành **"Xác thực: C# SSO Microservice (:5001)"**. Bấm Dashboard, dữ liệu doanh thu báo cáo tổng hợp hiển thị rõ nguồn từ **"C# Report Microservice (:5003)"**.
*   **Lời thoại**: *"Khi cụm C# hoạt động, Web Component sẽ gọi REST API liên thông xác thực SSO và thống kê báo cáo doanh thu trực tiếp từ các microservice C# cổng 5001 & 5003."*

#### 📍 Bước 7: Minh chứng tính bền vững dữ liệu (Persistence)
*   **Thao tác**: Tắt Docker Compose (`docker-compose down`) và bật lại. Tải lại trang Web, đăng nhập tài khoản `customer_test` và chứng minh các đơn hàng cũ vẫn tồn tại nguyên vẹn.
*   **Lời thoại**: *"Dữ liệu được lưu trữ bền vững vật lý tại tệp SQLite orders.db chứ không lưu tạm trên RAM, đảm bảo thông tin không bị mất đi khi restart hệ thống."*
