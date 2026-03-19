# app/models/order.py
from pydantic import BaseModel

class OrderRequest(BaseModel):
    product_id: int
    order_type: str = "standard" # standard | express
    address: str

class ObjectInformation(BaseModel):
    id: int
    details: str
    status: str
    tracking_code: str
