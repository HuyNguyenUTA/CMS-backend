# app/services/chatbot.py

import json
from openai import OpenAI
from app.models.chat import ChatPayload
from app.core.config import settings
from app.services.rag import retrieve_from_qdrant

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_chat_response(payload: ChatPayload, restaurant_id="sakura-ramen"):
    try:
        context = retrieve_from_qdrant(restaurant_id, payload.messages[-1].content)

        system_prompt = f"""
        You are Sakura, a friendly and helpful assistant at a ramen restaurant.

        Relevant menu info:
        {context}

        Your job is to:
        - Answer customer questions clearly and politely.
        - Do not confirm orders directly.
        - Summarize pending orders first and use JSON format.

        Examples:
        {{ "reply": "...", "pending_order": [{{"item": "...", "quantity": 1}}] }}
        {{ "reply": "...", "order": [{{"item": "...", "quantity": 1}}] }}
        {{ "reply": "..." }}
        """

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                *payload.messages
            ],
            temperature=0.7,
            max_tokens=300,
        )

        content = response.choices[0].message.content
        return json.loads(content) if content.startswith("{") else {"reply": content}

    except Exception as e:
        return {"reply": f"⚠️ Error: {str(e)}"}
