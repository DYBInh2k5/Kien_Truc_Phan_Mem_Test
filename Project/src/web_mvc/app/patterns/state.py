# app/patterns/state.py
from abc import ABC, abstractmethod

class OrderState(ABC):
    @abstractmethod
    def next_step(self, context) -> str:
        pass

    @abstractmethod
    def get_status_name(self) -> str:
        pass

class PendingState(OrderState):
    def next_step(self, context) -> str:
        context.set_state(PaidState())
        return "Đơn hàng đang chờ xử lý. Thanh toán thành công -> Đã Thanh Toán."

    def get_status_name(self) -> str:
        return "Pending"

class PaidState(OrderState):
    def next_step(self, context) -> str:
        context.set_state(ShippedState())
        return "Đơn hàng đã thanh toán. Bắt đầu vận chuyển -> Đang Giao Hàng."

    def get_status_name(self) -> str:
        return "Paid"

class ShippedState(OrderState):
    def next_step(self, context) -> str:
        return "Đơn hàng đã được giao."

    def get_status_name(self) -> str:
        return "Shipped"

class OrderContext:
    """
    STATE PATTERN
    Thay vì dùng if-else phức tạp để sửa trạng thái.
    Mỗi State tự quyết định chuyển đổi logic và thông tin của nó.
    """
    def __init__(self):
        self.state = PendingState()

    def set_state(self, state: OrderState):
        self.state = state

    def proceed(self) -> str:
        return self.state.next_step(self)

    def current_status(self) -> str:
        return self.state.get_status_name()
