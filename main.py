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

        # ✅ Load real restaurant menu
        with open("menu.txt", "r") as f:
            menu_text = f.read()

        system_prompt = f"""
        You are Sakura, a friendly and helpful assistant at a ramen restaurant.

        Here is the full menu and restaurant information:
        {menu_text}

        Your job is to:
        - Answer customer questions clearly and politely.
        - If the customer asks to place an order, do NOT confirm it right away.
        - Instead, respond with a message that summarizes the order and include a `pending_order` field.
        - Only include an `order` field after the customer explicitly confirms (e.g. they say "yes", "confirm", or "submit").

        Always reply in JSON format like:
        {{ "reply": "...", "pending_order": [{{"item": "...", "quantity": 1}}] }}

        When confirmed, respond like:
        {{ "reply": "...", "order": [{{"item": "...", "quantity": 1}}] }}

        If the user is just chatting or asking questions, respond with:
        {{ "reply": "..." }}

        Avoid hallucinating items. Only use menu items listed above.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                *payload.messages
            ],
            temperature=0.7,
            max_tokens=300,
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