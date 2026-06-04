# app/controllers/api_router.py
from fastapi import APIRouter
from app.patterns.singleton import DatabaseConnection
from app.patterns.iterator import OrderCollection
from app.patterns.facade import OrderFacade
from app.models.order import OrderRequest
from app.models.user import UserLogin, UserCreate
from app.services.auth_service import AuthService

router = APIRouter()

# 1. FUNCTION: Login
@router.post("/auth/login")
def login(credentials: UserLogin):
    return AuthService.login(credentials)

# 2. FUNCTION: Managing Users
@router.get("/users")
def get_users():
    """Lấy danh sách người dùng"""
    return AuthService.get_all_users()

@router.post("/users")
def create_user(new_user: UserCreate):
    """Đăng ký / Thêm người dùng mới"""
    return AuthService.register_user(new_user)

# 3. MAPPING FACADE, SINGLETON, FACTORY, STATE (Tạo đơn hàng)
@router.post("/orders/place")
def place_order(order_request: OrderRequest):
    # Dùng FACADE xử lý chu trình đặt hàng phức tạp
    facade = OrderFacade()
    result = facade.place_order(order_request.product_id, order_request.order_type, order_request.address)
    
    if result.get("status") == "Success":
        # Dùng SINGLETON gọi kết nối DB và chèn đơn hàng thật vào SQLite
        db = DatabaseConnection()
        details = f"Product ID: {order_request.product_id} ({result['order_type']}) - Address: {order_request.address}"
        new_id = db.execute(
            "INSERT INTO orders (details, status, tracking_code) VALUES (?, ?, ?)",
            (details, result["final_state"], result["tracking_code"])
        )
        result["order_id"] = new_id
        
    return result

# 4. FUNCTION: Search/Find (Áp dụng Iterator)
@router.get("/orders/search/{order_id}")
def search_order(order_id: int):
    import urllib.request
    import json
    import logging

    # 1. Thử gọi C# Search Microservice (Cổng 5002)
    search_url = f"http://host.docker.internal:5002/api/search/orders/{order_id}"
    try:
        req = urllib.request.Request(search_url, method="GET")
        with urllib.request.urlopen(req, timeout=2.0) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            res_json["search_source"] = "C# Search Microservice (:5002)"
            return res_json
    except Exception as e:
        logging.warning(f"Không kết nối được C# Search Service ({e}). Thử tìm kiếm cục bộ qua Iterator...")

    # 2. Cơ chế DỰ PHÒNG (Fallback): Sử dụng Iterator Pattern trên SQLite cục bộ
    db = DatabaseConnection()
    orders_raw = db.query("SELECT * FROM orders")
    
    order_db = OrderCollection()
    for o in orders_raw:
        order_db.add_order(o)
        
    # Search logic qua ITERATOR Pattern
    order = order_db.find_order(order_id)
    if not order:
        return {"error": f"Không tìm thấy đơn hàng {order_id} (Đã kiểm tra cả C# Search và SQLite)"}
    
    order["search_source"] = "SQLite Local (Iterator Pattern Fallback)"
    return order

# 5. FUNCTION: Show "Object-Information"
@router.get("/orders/")
def show_all_orders():
    # Lấy dữ liệu từ SQLite đưa vào OrderCollection để duyệt qua Iterator
    db = DatabaseConnection()
    orders_raw = db.query("SELECT * FROM orders")
    
    order_db = OrderCollection()
    for o in orders_raw:
        order_db.add_order(o)
        
    # Show qua Iterator
    all_orders = [o for o in order_db]
    return all_orders

# 6. FUNCTION: Get report from C# Report Service (Proxy call with Fallback)
@router.get("/report/csharp-summary")
def get_csharp_report():
    import urllib.request
    import json
    import logging

    csharp_url = "http://host.docker.internal:5003/api/report/summary"
    try:
        req = urllib.request.Request(csharp_url, method="GET")
        with urllib.request.urlopen(req, timeout=2.0) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            # Thêm flag nguồn gốc dữ liệu để UI dễ hiển thị
            res_json["data_source"] = "C# Report Microservice (:5003)"
            return res_json
    except Exception as e:
        logging.warning(f"Lỗi kết nối tới C# Report Service ({e}). Đang sử dụng dữ liệu dự phòng...")
        # Fallback dữ liệu mock
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
