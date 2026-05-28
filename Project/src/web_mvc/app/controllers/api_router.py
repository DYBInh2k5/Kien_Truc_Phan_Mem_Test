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
    # Lấy dữ liệu từ SQLite đưa vào OrderCollection để duyệt qua Iterator
    db = DatabaseConnection()
    orders_raw = db.query("SELECT * FROM orders")
    
    order_db = OrderCollection()
    for o in orders_raw:
        order_db.add_order(o)
        
    # Search logic qua ITERATOR Pattern
    order = order_db.find_order(order_id)
    if not order:
        return {"error": f"Không tìm thấy đơn hàng {order_id}"}
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
