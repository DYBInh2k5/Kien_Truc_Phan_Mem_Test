# app/patterns/facade.py
import time
from .factory import OrderFactory
from .state import OrderContext

# =========================================================================
# SUBSYSTEMS (Các hệ thống con phức tạp)
# Chứa các logic xử lý nghiệp vụ đơn lẻ trong chuỗi quy trình mua sắm.
# =========================================================================

class InventorySystem:
    """Hệ thống quản lý tồn kho hàng hóa"""
    def check_stock(self, product_id: int) -> bool:
        # Giả lập hoạt động kiểm tra tồn kho
        print(f"Inventory: Đang kiểm tra tồn kho cho sản phẩm {product_id}...")
        return True # Giả lập: Hàng luôn còn trong kho

class PaymentSystem:
    """Hệ thống xử lý cổng thanh toán trực tuyến"""
    def process_payment(self, amount: float) -> bool:
        # Giả lập kết nối cổng ngân hàng/ví điện tử và trừ tiền
        print(f"Payment: Đang xử lý giao dịch thanh toán số tiền ${amount}...")
        return True # Giả lập: Giao dịch thanh toán luôn thành công

class ShippingSystem:
    """Hệ thống điều phối vận đơn và đối tác vận chuyển"""
    def arrange_shipping(self, product_id: int, address: str) -> str:
        # Giả lập đăng ký thông tin giao hàng và lấy mã tracking vận chuyển
        print(f"Shipping: Đang thiết lập vận đơn giao sản phẩm {product_id} tới địa chỉ: {address}")
        return f"TRACK_EXPRESS_{int(time.time())}" # Sinh mã vận đơn động theo mốc thời gian

# =========================================================================
# FACADE CLASS (Lớp mặt tiền che giấu sự phức tạp)
# FACADE PATTERN (Structural Design Pattern - Nhóm Cấu trúc)
# =========================================================================
class OrderFacade:
    """
    Cung cấp một phương thức đơn giản duy nhất là `place_order` để bao bọc và điều phối
    các bước nghiệp vụ phức tạp của các hệ thống con bên dưới (Inventory, Payment, Shipping).
    
    1. Lợi ích:
       - Giúp giảm sự phụ thuộc chéo (Loose Coupling). Tầng Controller gọi đặt hàng chỉ cần gọi Facade
         mà không cần biết trình tự tương tác hoặc cấu trúc của các hệ thống con.
       - Giúp mã nguồn Controller vô cùng ngắn gọn, dễ đọc, dễ kiểm thử.
       
    2. Quy trình tích hợp Patterns chéo:
       - Facade gọi Factory Method (`OrderFactory`) để khởi tạo thực thể đơn hàng phù hợp và tính phí ship.
       - Facade khởi tạo máy trạng thái (`OrderContext` của State Pattern) để theo dõi và chuyển dịch trạng thái đơn hàng.
       - Facade phối hợp gọi các Subsytems: check kho -> thanh toán (đổi trạng thái sang Paid) -> giao hàng (đổi sang Shipped).
    """
    def __init__(self):
        # Khởi tạo các hệ thống con trực tiếp bên trong Facade
        self.inventory = InventorySystem()
        self.payment = PaymentSystem()
        self.shipping = ShippingSystem()

    def place_order(self, product_id: int, order_type: str, address: str) -> dict:
        print("\n--- [FACADE] Bắt đầu quy trình đặt hàng tích hợp ---")
        
        # 1. Sử dụng FACTORY METHOD PATTERN để tạo đúng loại đơn hàng và tính phí vận chuyển tương ứng
        order = OrderFactory.create_order(product_id, order_type)
        
        # 2. Sử dụng STATE PATTERN để khởi tạo ngữ cảnh trạng thái đơn hàng ban đầu (Mặc định: Pending)
        order_process = OrderContext()
        print(f"[STATE] Trạng thái khởi tạo: {order_process.current_status()}")
        
        # 3. Bước 1 nghiệp vụ: Kiểm kho (Inventory Subsystem)
        if not self.inventory.check_stock(product_id):
            return {"status": "Failed", "reason": "Sản phẩm đã hết hàng trong hệ thống kho"}
        
        # 4. Bước 2 nghiệp vụ: Xử lý trừ tiền thanh toán (Payment Subsystem)
        shipping_cost = order.get_shipping_cost()
        if not self.payment.process_payment(shipping_cost):
            return {"status": "Failed", "reason": "Thanh toán giao dịch thất bại"}

        # Cập nhật trạng thái đơn hàng sang "Paid" sau khi thanh toán thành công thông qua State Pattern
        msg_paid = order_process.proceed()
        print(f"[STATE] {msg_paid}")

        # 5. Bước 3 nghiệp vụ: Thiết lập giao nhận và lấy mã vận đơn (Shipping Subsystem)
        tracking_code = self.shipping.arrange_shipping(product_id, address)
        
        # Cập nhật trạng thái đơn hàng sang "Shipped" sau khi giao vận chuyển thành công thông qua State Pattern
        msg_shipped = order_process.proceed()
        print(f"[STATE] {msg_shipped}")

        # Trả về kết quả hoàn chỉnh đã đóng gói cho Controller để ghi vào SQLite
        return {
            "status": "Success",
            "order_type": order.get_order_type(),
            "final_state": order_process.current_status(),
            "tracking_code": tracking_code
        }
