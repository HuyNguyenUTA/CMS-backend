from fastapi import APIRouter
from app.models.order import OrderPayload

router = APIRouter()

@router.post("/")
async def submit_order(order: OrderPayload):
    print("📦 Order received:", order)

    item_list = ", ".join([f"{item.quantity}x {item.item}" for item in order.items])
    return {
        "status": "success",
        "message": f"Order confirmed for {item_list} totaling ${order.total:.2f}."
    }
