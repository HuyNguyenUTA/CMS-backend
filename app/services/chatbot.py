import json
from openai import OpenAI
from app.models.chat import ChatPayload
from app.core.config import settings

async def generate_chat_response(payload: ChatPayload):
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        with open("data/menu.txt", "r") as f:
            menu_text = f.read()

        system_prompt = f"""
        You are Sakura, a friendly assistant at a ramen restaurant.

        MENU:
        {menu_text}

        Respond in JSON like:
        {{ "reply": "...", "pending_order": [{{"item": "...", "quantity": 1}}] }}

        If confirmed:
        {{ "reply": "...", "order": [{{"item": "...", "quantity": 1}}] }}

        Just chatting:
        {{ "reply": "..." }}
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
            return json.loads(content)
        except json.JSONDecodeError:
            return { "reply": content }

    except Exception as e:
        return {"reply": f"⚠️ Error: {str(e)}"}
