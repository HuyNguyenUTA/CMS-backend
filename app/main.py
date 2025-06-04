from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, order
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(order.router, prefix="/order", tags=["Order"])
