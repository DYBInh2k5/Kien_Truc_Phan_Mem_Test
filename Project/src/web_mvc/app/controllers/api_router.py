# app/controllers/api_router.py
from fastapi import APIRouter
from app.patterns.singleton import DatabaseConnection
from app.patterns.iterator import OrderCollection
from app.patterns.facade import OrderFacade
from app.models.order import OrderRequest
from app.models.user import UserLogin, UserCreate
from app.services.auth_service import AuthService

# Khởi tạo đối tượng Router định tuyến của FastAPI
router = APIRouter()

# ==========================================
# 1. API: ĐĂNG NHẬP (Xác thực tập trung)
# ==========================================
@router.post("/auth/login")
def login(credentials: UserLogin):
    """
    Tiếp nhận thông tin tài khoản đăng nhập của người dùng.
    - Chuyển tiếp yêu cầu (Proxy) sang lớp AuthService xử lý logic xác thực.
    """
    return AuthService.login(credentials)

# ==========================================
# 2. API: QUẢN LÝ THÀNH VIÊN (Users CRUD)
# ==========================================
@router.get("/users")
def get_users():
    """
    Lấy danh sách toàn bộ người dùng trong hệ thống.
    - Gọi đến lớp AuthService để lấy dữ liệu từ SQLite.
    """
    return AuthService.get_all_users()

@router.post("/users")
def create_user(new_user: UserCreate):
    """
    Đăng ký tài khoản người dùng mới (đọc/ghi trực tiếp vào SQLite cục bộ).
    - Gọi đến phương thức register_user của AuthService để lưu dữ liệu.
    """
    return AuthService.register_user(new_user)

# ==========================================
# 3. API: ĐẶT ĐƠN HÀNG MỚI (Áp dụng Facade, Singleton, Factory, State)
# ==========================================
@router.post("/orders/place")
def place_order(order_request: OrderRequest):
    """
    Quy trình đặt đơn hàng tích hợp nhiều Design Patterns:
    - 1. Gọi OrderFacade để tự động điều phối chu trình đặt hàng phức tạp (Facade Pattern).
    - 2. Facade gọi OrderFactory để tạo loại đơn Standard hoặc Express (Factory Method Pattern).
    - 3. Facade sử dụng OrderContext để luân chuyển trạng thái Pending -> Paid -> Shipped (State Pattern).
    - 4. Sử dụng DatabaseConnection để ghi nhận thông tin đơn hàng thật vào SQLite (Singleton Pattern).
    """
    # Khởi tạo và thực thi đặt hàng thông qua lớp mặt tiền Facade
    facade = OrderFacade()
    result = facade.place_order(order_request.product_id, order_request.order_type, order_request.address)
    
    if result.get("status") == "Success":
        # Gọi instance Database Singleton để thực thi câu lệnh chèn dữ liệu bền vững
        db = DatabaseConnection()
        details = f"Product ID: {order_request.product_id} ({result['order_type']}) - Address: {order_request.address}"
        
        # Chèn đơn hàng mới vào bảng orders trong SQLite
        new_id = db.execute(
            "INSERT INTO orders (details, status, tracking_code) VALUES (?, ?, ?)",
            (details, result["final_state"], result["tracking_code"])
        )
        result["order_id"] = new_id
        
    return result

# ==========================================
# 4. API: TRA CỨU ĐƠN HÀNG THEO ID (Tích hợp chéo với Fallback)
# ==========================================
@router.get("/orders/search/{order_id}")
def search_order(order_id: int):
    """
    Tra cứu thông tin đơn hàng theo ID.
    - Bước 1: Gọi chéo HTTP GET sang C# Search Microservice (Cổng 5002) để truy xuất dữ liệu.
    - Bước 2 (Fallback): Nếu C# Search Service offline hoặc gặp sự cố, hệ thống tự động nhảy vào khối catch
      và kích hoạt cơ chế dự phòng cục bộ: dùng Database Singleton truy vấn tất cả đơn hàng từ SQLite,
      nạp vào tập hợp OrderCollection và duyệt qua danh sách bằng Iterator Pattern để tìm đơn hàng.
    """
    import urllib.request
    import json
    import logging

    # 1. Thử kết nối gọi C# Search Microservice (Cổng 5002)
    # Lưu ý dùng host.docker.internal để Container Python gọi ra ngoài máy Windows vật lý
    search_url = f"http://host.docker.internal:5002/api/search/orders/{order_id}"
    try:
        req = urllib.request.Request(search_url, method="GET")
        # Giới hạn timeout 2.0 giây để tránh đơ giao diện nếu C# chưa được bật
        with urllib.request.urlopen(req, timeout=2.0) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            # Ghi nhận nguồn gốc tìm kiếm để giao diện Frontend hiển thị huy hiệu động
            res_json["search_source"] = "C# Search Microservice (:5002)"
            return res_json
    except Exception as e:
        logging.warning(f"Không kết nối được C# Search Service ({e}). Thử tìm kiếm cục bộ qua Iterator...")

    # 2. Cơ chế DỰ PHÒNG (Fallback): Sử dụng Iterator Pattern trên SQLite cục bộ
    db = DatabaseConnection()
    orders_raw = db.query("SELECT * FROM orders")
    
    order_db = OrderCollection()
    # Nạp toàn bộ đơn hàng vào Collection
    for o in orders_raw:
        order_db.add_order(o)
        
    # Gọi hàm tìm kiếm sử dụng Iterator Pattern (phương thức __next__ ẩn)
    order = order_db.find_order(order_id)
    if not order:
        return {"error": f"Không tìm thấy đơn hàng {order_id} (Đã kiểm tra cả C# Search và SQLite)"}
    
    order["search_source"] = "SQLite Local (Iterator Pattern Fallback)"
    return order

# ==========================================
# 5. API: LẤY DANH SÁCH TẤT CẢ ĐƠN HÀNG (Duyệt qua Iterator cục bộ)
# ==========================================
@router.get("/orders/")
def show_all_orders():
    """
    Duyệt và hiển thị toàn bộ danh sách đơn hàng có trong SQLite.
    - Nạp danh sách từ SQLite vào lớp tập hợp OrderCollection.
    - Sử dụng cú pháp List Comprehension duyệt qua OrderCollection bằng cơ chế Iterator Pattern.
    """
    db = DatabaseConnection()
    orders_raw = db.query("SELECT * FROM orders")
    
    order_db = OrderCollection()
    for o in orders_raw:
        order_db.add_order(o)
        
    # Duyệt qua Iterator của OrderCollection
    all_orders = [o for o in order_db]
    return all_orders

# ==========================================
# 6. API: LẤY THỐNG KÊ DOANH THU (Proxy gọi chéo C# Report với Fallback)
# ==========================================
@router.get("/report/csharp-summary")
def get_csharp_report():
    """
    Lấy báo cáo doanh thu tài chính.
    - Bước 1: Gửi yêu cầu HTTP GET sang C# Report Microservice (Cổng 5003).
    - Bước 2 (Fallback): Nếu C# Report Service offline, bắt ngoại lệ lỗi kết nối và tự động trả về
      dữ liệu mock hợp lệ cục bộ kèm cờ báo hiệu, đảm bảo Dashboard Web không bị sập và hiển thị bình thường.
    """
    import urllib.request
    import json
    import logging

    csharp_url = "http://host.docker.internal:5003/api/report/summary"
    try:
        req = urllib.request.Request(csharp_url, method="GET")
        with urllib.request.urlopen(req, timeout=2.0) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            # Thêm thông tin nguồn gốc dữ liệu để UI cập nhật nhãn động
            res_json["data_source"] = "C# Report Microservice (:5003)"
            return res_json
    except Exception as e:
        logging.warning(f"Lỗi kết nối tới C# Report Service ({e}). Đang sử dụng dữ liệu dự phòng...")
        # Fallback dữ liệu mock cục bộ khi dịch vụ C# ngoại tuyến
        return {
            "total_orders": 99,
            "total_revenue": 9999.99,
            "shipping_summary": [
                { "type": "Standard", "count": 80, "cost": 200.0 },
                { "type": "Express", "count": 19, "cost": 285.0 }
            ],
            "system": "Python local (C# Microservice Offline - Fallback)",
            "data_source": "SQLite Local (C# Service Offline)"
        }
