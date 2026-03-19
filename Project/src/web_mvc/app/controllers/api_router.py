# app/controllers/api_router.py
from fastapi import APIRouter
from app.patterns.singleton import DatabaseConnection
from app.patterns.iterator import OrderCollection
from app.patterns.facade import OrderFacade
from app.models.order import OrderRequest
from app.models.user import UserLogin, UserCreate
from app.services.auth_service import AuthService

router = APIRouter()

# --- MOCK DATA FOR ORDER SEARCH ---
mock_order_db = OrderCollection()
mock_order_db.add_order({"id": 101, "details": "Laptop XYZ", "status": "Shipped", "tracking_code": "TRACK_999"})
mock_order_db.add_order({"id": 102, "details": "Bàn Phím Cơ", "status": "Pending", "tracking_code": "TRACK_333"})

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
    # Dùng SINGLETON gọi kết nối DB
    db = DatabaseConnection() # Chạy log xem có đang dùng 1 connect duy nhất ko
    db.query("INSERT INTO TempData...")

    # Dùng FACADE xử lý chu trình đặt hàng phức tạp
    facade = OrderFacade()
    return facade.place_order(order_request.product_id, order_request.order_type, order_request.address)

# 4. FUNCTION: Search/Find (Áp dụng Iterator)
@router.get("/orders/search/{order_id}")
def search_order(order_id: int):
    # Search logic qua ITERATOR Pattern
    order = mock_order_db.find_order(order_id)
    if not order:
        return {"error": f"Không tìm thấy đơn hàng {order_id}"}
    return order

# 5. FUNCTION: Show "Object-Information"
@router.get("/orders/")
def show_all_orders():
    # Show qua Iterator
    all_orders = [o for o in mock_order_db]
    return all_orders
