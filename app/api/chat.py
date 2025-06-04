from fastapi import APIRouter
from app.models.chat import ChatPayload
from app.services.chatbot import generate_chat_response

router = APIRouter()

@router.post("/")
async def chat(payload: ChatPayload):
    return await generate_chat_response(payload)
