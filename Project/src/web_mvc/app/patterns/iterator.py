# app/patterns/iterator.py

# ==========================================
# COLLECTION & ITERATOR CLASS (Lớp bộ sưu tập tích hợp bộ duyệt)
# ITERATOR PATTERN (Behavioral Design Pattern - Nhóm Hành vi)
# ==========================================
class OrderCollection:
    """
    Quản lý một tập hợp danh sách các đơn hàng và cung cấp cơ chế duyệt qua chúng.
    
    1. Mục đích:
       - Cung cấp một cách để truy cập tuần tự vào các phần tử của một đối tượng tập hợp
         mà không làm lộ cấu trúc biểu diễn bên trong của tập hợp đó (ví dụ: cấu trúc mảng, cây, bảng băm).
         
    2. Kỹ thuật cài đặt trong Python:
       - Triển khai phương thức chuẩn `__iter__()` để trả về chính đối tượng Collection và khởi tạo chỉ số chạy (`_index = 0`).
       - Triển khai phương thức chuẩn `__next__()` để trả về phần tử tiếp theo của danh sách hoặc ném ra ngoại lệ
         `StopIteration` khi đã duyệt hết phần tử để báo hiệu dừng vòng lặp `for...in`.
         
    3. Lợi ích:
       - Che giấu cấu trúc mảng `_orders` lưu trữ thực tế bên trong. Nếu sau này chúng ta nâng cấp cấu trúc lưu trữ
         (từ mảng sang cây nhị phân để tìm kiếm nhanh hơn), tầng gọi bên ngoài sử dụng vòng lặp `for...in`
         sẽ hoàn toàn không bị ảnh hưởng hay phải sửa code.
    """
    def __init__(self):
        # Cấu trúc lưu trữ nội bộ (hiện tại là kiểu list/mảng thông thường)
        self._orders = []

    def add_order(self, order_data: dict):
        """Thêm một đơn hàng mới vào bộ sưu tập"""
        self._orders.append(order_data)

    def __iter__(self):
        """Khởi tạo chỉ số duyệt khi bắt đầu vòng lặp"""
        self._index = 0
        return self

    def __next__(self):
        """Trả về phần tử tiếp theo trong quá trình duyệt"""
        if self._index < len(self._orders):
            result = self._orders[self._index]
            self._index += 1
            return result
        # Ném ra StopIteration khi đã duyệt hết mảng để dừng vòng lặp
        raise StopIteration

    def find_order(self, order_id: int):
        """
        Sử dụng bộ duyệt (Iterator) của chính Class để thực hiện tìm kiếm đơn hàng theo ID.
        - `for order in self` kích hoạt việc gọi tuần tự đến `__next__` của đối tượng.
        - Trả về: Dictionary thông tin đơn hàng nếu thấy, hoặc None nếu không tìm thấy.
        """
        for order in self:
            if order.get("id") == order_id:
                return order
        return None
