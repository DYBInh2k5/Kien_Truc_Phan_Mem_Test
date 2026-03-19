# Tài Liệu Thiết Kế (Architecture Document) - Hệ Thống Quản Lý Đơn Hàng

## 1. Problem Description (Mô tả bài toán)
Hệ thống quản lý đơn hàng gặp thách thức về tính mở rộng khi nghiệp vụ xử lý đơn hàng phức tạp dần lên (phải tương tác với kho hàng, thanh toán, giao vận, xuất báo cáo...). Quản lý trạng thái đơn hàng (Đang chờ -> Đã thanh toán -> Đã giao) bằng cấu trúc lệnh `if/else` truyền thống dễ gây ra mã nguồn phức tạp (Spaghetti code) và khó bảo trì.
Ngoài ra, cần đảm bảo ứng dụng có thể chịu tải dưới kiến trúc n-Tiers (MVC) và giao tiếp với các Microservices độc lập (ví dụ: SSO - Single Sign On) thông qua API REST.

---

## 2. System Diagram (Component / Deployment Diagram)

Sơ đồ triển khai hệ thống cho thấy Cụm MVC phục vụ Client và kết nối với các Microservices nội bộ.

```mermaid
graph TD
    Client((Client App / Browser))

    subgraph MVC_nLayers_Web_Component
        Controller[Controllers & Routers]
        Service[Services Layer]
        Repository[Repositories / Database]
        
        Controller --> Service
        Service --> Repository
    end

    subgraph Microservices_Component
        SSO[Auth SSO Service]
        Report[Statistical Report Service]
        Search[Search API Service]
    end

    Client -- HTTP/REST --> Controller
    Controller -- gRPC / REST --> SSO
    Service -- gRPC / REST --> Search
    Service -- gRPC / REST --> Report
    Repository -.-> DB[(Main Database)]
```

---

## 3. Class Diagram (1st details - Thiết kế ban đầu chưa có Pattern)

Trước khi áp dụng Pattern, logic tạo hóa đơn và xử lý trạng thái bị dồn hết vào class `OrderService`, gây phình to mã nguồn (God/Monster Object).

```mermaid
classDiagram
    class OrderController {
        +placeOrder(productId, type, address)
        +changeStatus(orderId, status)
    }
    class OrderService {
        +dbConn
        +inventoryApi
        +paymentApi
        +createOrder(productId, type, address)
        +updateStatus(orderId, newStatus)
    }
    class Order {
        +id
        +type
        +status
        +shipping_cost
    }

    OrderController --> OrderService
    OrderService ..> Order : creates/updates
```

---

## 4. Class Diagram (Final Design - Áp dụng 5 Design Patterns)
Sự kết nối giữa các Tầng (Controller, Service, Models, Config) khi nhúng 5 Patterns.

```mermaid
classDiagram
    %% ======= PATTERNS ======= %%
    class DatabaseConnection {
        <<Singleton>>
        - _instance : static
        - is_connected
        + get_connection()
        + query()
    }

    class OrderFactory {
        <<Factory Method>>
        + create_order(type) : Order
    }

    class OrderFacade {
        <<Facade>>
        - inventorySystem
        - paymentSystem
        - shippingSystem
        + place_order()
    }

    class OrderState {
        <<State - Interface>>
        + next_step(context)
        + get_status_name()
    }

    class OrderContext {
        <<State Context>>
        - state: OrderState
        + set_state()
        + proceed()
    }

    class OrderCollection {
        <<Iterator>>
        - orders
        + __iter__()
        + __next__()
        + find_order()
    }

    %% ======= CLASSES ======= %%
    class OrderController {
        + login()
        + search_order()
        + place_order()
    }
    
    class Order {
        <<Abstract Model>>
        + get_shipping_cost()
    }
    class StandardOrder { }
    class ExpressOrder { }
    
    Order <|-- StandardOrder
    Order <|-- ExpressOrder

    OrderState <|-- PendingState
    OrderState <|-- PaidState
    OrderState <|-- ShippedState

    %% ======= RELATIONSHIPS ======= %%
    OrderController --> OrderFacade : uses
    OrderController --> OrderCollection : traverses
    OrderController --> DatabaseConnection : access DB

    OrderFacade --> OrderFactory : uses
    OrderFacade --> OrderContext : runs
    OrderFactory ..> Order : creates
    OrderContext o--> OrderState : holds State
```

---

## 5. Detail Diagrams (Sequence: Trạng thái Đơn hàng 1st vs Final)

Yêu cầu vẽ 2 Detail diagram dùng để phân tích lợi ích của 1 Mẫu (State Pattern).

### 5.1. 1st Diagram: Quy trình Đặt hàng lúc CHƯA có Facade và State Pattern
Chữ kí của sơ đồ là Client phải gọi từng hàm lẻ tẻ để kiểm kho, trả tiền và gửi yêu cầu, sau đó dùng `if` lồng để chỉnh trạng thái.

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

### 5.2. Final Diagram: Quy trình Đặt hàng ĐÃ áp dụng Facade + State Pattern
Client làm việc ở mức rất trừu tượng. Facade che giấu sự phức tạp của Payment/Inventory. State tự quyết định vòng đời của đơn hàng.

```mermaid
sequenceDiagram
    participant C as OrderController
    participant F as OrderFacade (Structural)
    participant ST as OrderContext (Behavioral)
    
    C->>F: place_order(product_id, type)
    
    F->>F: inventory.check()
    F->>F: payment.process()
    
    F->>ST: new OrderContext()
    note over ST: State starts at PendingState

    F->>ST: proceed()
    note over ST: PendingState upgrades context to PaidState
    
    F->>ST: proceed()
    note over ST: PaidState upgrades context to ShippedState
    
    F-->>C: return {status: Success, final_state: Shipped}
```
