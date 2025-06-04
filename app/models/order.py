# schemas/order.py
from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    item: str
    quantity: int

class OrderPayload(BaseModel):
    items: List[OrderItem]
    total: float
