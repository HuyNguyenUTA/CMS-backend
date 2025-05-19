from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import json
import os
import openai
from schemas.order import OrderPayload
from schemas.chat import ChatPayload



load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(payload: ChatPayload):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are Sakura, a friendly restaurant assistant. "
                    "Always respond in JSON format like: "
                    "{\"reply\": \"Your message here.\", \"order\": [...] (optional)}. "
                    "Only include the 'order' field if the user places an order. "
                    "Otherwise just provide a reply message."
                )
},
                *payload.messages
            ],
            temperature=0.7,
            max_tokens=200,
        )

        content = response.choices[0].message.content

        try:
            parsed = json.loads(content)
            return parsed
        except json.JSONDecodeError:
            return { "reply": content }

    except Exception as e:
        return {"reply": f"⚠️ Error: {str(e)}"}


@app.post("/order")
async def submit_order(order: OrderPayload):
    # Here you could forward to POS or just log it
    print("📦 Order received:", order)

    item_list = ", ".join([f"{item.quantity}x {item.item}" for item in order.items])
    return {
        "status": "success",
        "message": f"Order confirmed for {item_list} totaling ${order.total:.2f}."
    }