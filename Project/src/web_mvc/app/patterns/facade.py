# app/patterns/facade.py
import time
from .factory import OrderFactory
from .state import OrderContext

# --- Subsystems ---
class InventorySystem:
    def check_stock(self, product_id: int) -> bool:
        print(f"Inventory: Checking stock for product {product_id}...")
        return True # Giả sử luôn còn hàng

class PaymentSystem:
    def process_payment(self, amount: float) -> bool:
        print(f"Payment: Processing amount ${amount}...")
        return True # Thanh toán thành công

class ShippingSystem:
    def arrange_shipping(self, product_id: int, address: str) -> str:
        print(f"Shipping: Arranging delivery for product {product_id} to {address}")
        return f"Tracking_Code_{int(time.time())}"

# --- Facade ---
class OrderFacade:
    """
    FACADE PATTERN (Structural Pattern)
    Bao bọc các subsystem phức tạp (Inventory, Payment, Shipping)
    cung cấp 1 interface đơn giản cho Controller/Client giao tiếp.
    """
    def __init__(self):
        self.inventory = InventorySystem()
        self.payment = PaymentSystem()
        self.shipping = ShippingSystem()

    def place_order(self, product_id: int, order_type: str, address: str) -> dict:
        print("\n--- Bắt đầu quy trình đặt hàng qua Facade ---")
        
        # 1. Factory tạo đơn hàng
        order = OrderFactory.create_order(product_id, order_type)
        
        # 2. Khởi tạo State ban đầu
        order_process = OrderContext()
        print(f"Current State: {order_process.current_status()}")

        # 3. Kiểm tra kho (Inventory)
        if not self.inventory.check_stock(product_id):
            return {"status": "Failed", "reason": "Sản phẩm hết hàng"}
        
        # 4. Thanh toán (Payment)
        shipping_cost = order.get_shipping_cost()
        if not self.payment.process_payment(shipping_cost):
            return {"status": "Failed", "reason": "Thanh toán giao dịch thất bại"}

        # Cập nhật State sau khi thanh toán
        msg = order_process.proceed()
        print(msg)

        # 5. Giao hàng (Shipping)
        tracking_code = self.shipping.arrange_shipping(product_id, address)
        
        # Cập nhật State thành Đang Giao
        msg = order_process.proceed()
        print(msg)

        # Trả về kết quả cho Controller
        return {
            "status": "Success",
            "order_type": order.get_order_type(),
            "final_state": order_process.current_status(),
            "tracking_code": tracking_code
        }
