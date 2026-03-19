# app/patterns/factory.py
from abc import ABC, abstractmethod

# Product Interface
class Order(ABC):
    def __init__(self, product_id: int):
        self.product_id = product_id

    @abstractmethod
    def get_shipping_cost(self) -> float:
        pass

    @abstractmethod
    def get_order_type(self) -> str:
        pass

# Concrete Products
class StandardOrder(Order):
    def get_shipping_cost(self) -> float:
        return 2.5  # Phí giao hàng thường

    def get_order_type(self) -> str:
        return "Standard"

class ExpressOrder(Order):
    def get_shipping_cost(self) -> float:
        return 15.0 # Phí giao hàng hỏa tốc

    def get_order_type(self) -> str:
        return "Express"

# Factory Class
class OrderFactory:
    """
    FACTORY METHOD PATTERN
    Tạo ra các đối tượng Order khác nhau (Standard, Express) mà không phụ thuộc vào lớp cụ thể.
    """
    @staticmethod
    def create_order(product_id: int, order_type: str) -> Order:
        if order_type.lower() == 'express':
            return ExpressOrder(product_id)
        elif order_type.lower() == 'standard':
            return StandardOrder(product_id)
        raise ValueError("Invalid order type")
