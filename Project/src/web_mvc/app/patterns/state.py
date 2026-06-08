# app/patterns/state.py
from abc import ABC, abstractmethod

# =========================================================================
# STATE INTERFACE (Lớp giao diện trạng thái trừu tượng)
# Định nghĩa các phương thức chuyển trạng thái bắt buộc cho mọi State con
# =========================================================================
class OrderState(ABC):
    @abstractmethod
    def next_step(self, context) -> str:
        """Thực hiện chuyển dịch sang trạng thái tiếp theo dựa trên ngữ cảnh (context)"""
        pass

    @abstractmethod
    def get_status_name(self) -> str:
        """Trả về tên định danh của trạng thái hiện tại (Pending, Paid, Shipped)"""
        pass

# =========================================================================
# CONCRETE STATES (Các lớp trạng thái cụ thể)
# Mỗi lớp tự chịu trách nhiệm định nghĩa logic chuyển đổi trạng thái của chính nó.
# =========================================================================

class PendingState(OrderState):
    """Trạng thái Chờ Xử lý: Đơn hàng mới khởi tạo, chờ thanh toán"""
    def next_step(self, context) -> str:
        # Chuyển đổi trạng thái hiện tại của Context sang Đã Thanh Toán (PaidState)
        context.set_state(PaidState())
        return "Đơn hàng đang ở trạng thái Chờ xử lý. Thanh toán thành công -> Chuyển sang Đã Thanh Toán."

    def get_status_name(self) -> str:
        return "Pending"

class PaidState(OrderState):
    """Trạng thái Đã Thanh Toán: Đã trừ tiền thành công, chờ giao đơn vị vận chuyển"""
    def next_step(self, context) -> str:
        # Chuyển đổi trạng thái hiện tại của Context sang Đang Giao Hàng (ShippedState)
        context.set_state(ShippedState())
        return "Đơn hàng đã thanh toán xong. Bắt đầu liên hệ vận chuyển -> Chuyển sang Đang Giao Hàng."

    def get_status_name(self) -> str:
        return "Paid"

class ShippedState(OrderState):
    """Trạng thái Đang Giao Hàng: Vận đơn đã được tạo và đang đi giao"""
    def next_step(self, context) -> str:
        # Đã là trạng thái cuối cùng của quy trình đặt hàng
        return "Đơn hàng đã được bàn giao thành công cho bên vận chuyển. Đạt trạng thái cuối."

    def get_status_name(self) -> str:
        return "Shipped"

# =========================================================================
# CONTEXT CLASS (Lớp ngữ cảnh quản lý trạng thái)
# STATE PATTERN (Behavioral Design Pattern - Nhóm Hành vi)
# =========================================================================
class OrderContext:
    """
    Quản lý một đối tượng trạng thái hiện tại (OrderState) và điều hướng hành vi của nó.
    
    1. Lợi ích:
       - Loại bỏ hoàn toàn các cấu trúc lệnh rẽ nhánh `if/else` hoặc `switch-case` lồng nhau phức tạp
         để kiểm tra điều kiện nâng cấp trạng thái.
       - Tuân thủ nguyên lý Single Responsibility: Mỗi class State chỉ giải quyết logic chuyển đổi của nó.
       - Dễ mở rộng: Khi cần thêm các trạng thái mới (như Canceled, Refunded, Delivered), chỉ cần viết thêm
         Class mới kế thừa từ OrderState mà hoàn toàn không ảnh hưởng đến mã nguồn của các trạng thái cũ.
    """
    def __init__(self):
        # Trạng thái mặc định ban đầu khi tạo ngữ cảnh là Chờ Duyệt (PendingState)
        self.state = PendingState()

    def set_state(self, state: OrderState):
        """Thay đổi trạng thái hiện tại của ngữ cảnh"""
        self.state = state

    def proceed(self) -> str:
        """Thực thi bước chuyển dịch trạng thái tiếp theo"""
        return self.state.next_step(self)

    def current_status(self) -> str:
        """Lấy chuỗi định danh trạng thái hiện tại để hiển thị hoặc lưu DB"""
        return self.state.get_status_name()
