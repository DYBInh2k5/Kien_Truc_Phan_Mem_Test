# app/patterns/iterator.py

class OrderCollection:
    """
    ITERATOR PATTERN
    Dùng để duyệt qua một danh sách các Đơn hàng (hoặc Object-Information) trả về từ Database
    mà không để lộ cấu trúc bên trong.
    """
    def __init__(self):
        self._orders = []

    def add_order(self, order_data: dict):
        self._orders.append(order_data)

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._orders):
            result = self._orders[self._index]
            self._index += 1
            return result
        raise StopIteration

    def find_order(self, order_id: int):
        # Sử dụng Iterator để tìm đơn hàng
        for order in self:
            if order.get("id") == order_id:
                return order
        return None
