# app/patterns/factory.py
from abc import ABC, abstractmethod

# ==========================================
# PRODUCT INTERFACE (Lớp giao diện sản phẩm trừu tượng)
# Định nghĩa khung sườn cho các loại đơn hàng khác nhau
# ==========================================
class Order(ABC):
    def __init__(self, product_id: int):
        self.product_id = product_id

    @abstractmethod
    def get_shipping_cost(self) -> float:
        """Phương thức trừu tượng trả về chi phí vận chuyển của đơn hàng"""
        pass

    @abstractmethod
    def get_order_type(self) -> str:
        """Phương thức trừu tượng trả về tên loại vận chuyển (Standard/Express)"""
        pass

# ==========================================
# CONCRETE PRODUCTS (Các lớp sản phẩm cụ thể)
# Triển khai các phương thức cụ thể tương ứng với từng loại đơn hàng
# ==========================================

class StandardOrder(Order):
    """Đơn hàng vận chuyển thường (Standard Shipping)"""
    def get_shipping_cost(self) -> float:
        return 2.5  # Phí giao hàng thường là $2.5

    def get_order_type(self) -> str:
        return "Standard"

class ExpressOrder(Order):
    """Đơn hàng vận chuyển hỏa tốc (Express Shipping)"""
    def get_shipping_cost(self) -> float:
        return 15.0 # Phí giao hàng hỏa tốc là $15.0

    def get_order_type(self) -> str:
        return "Express"

# ==========================================
# FACTORY CLASS (Lớp nhà máy khởi tạo đối tượng)
# FACTORY METHOD PATTERN (Creational Design Pattern - Nhóm Khởi tạo)
# ==========================================
class OrderFactory:
    """
    Quyết định việc tạo ra loại đối tượng đơn hàng nào dựa vào tham số đầu vào.
    - Giúp tầng gọi (ví dụ: Facade hay Controller) không cần biết chi tiết khởi tạo của StandardOrder hay ExpressOrder.
    - Đảm bảo tính mở rộng cao (Open/Closed Principle): Khi cần thêm phương thức vận chuyển mới (ví dụ: Plane, Drone),
      chỉ cần tạo Class mới kế thừa Order và thêm nhánh điều kiện trong Factory, hoàn toàn không sửa code cũ ở Controller.
    """
    @staticmethod
    def create_order(product_id: int, order_type: str) -> Order:
        if order_type.lower() == 'express':
            return ExpressOrder(product_id)
        elif order_type.lower() == 'standard':
            return StandardOrder(product_id)
        raise ValueError("Loại đơn hàng không hợp lệ. Chỉ chấp nhận 'standard' hoặc 'express'.")
