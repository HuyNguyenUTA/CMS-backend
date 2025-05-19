from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import openai

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

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(payload: ChatRequest):
    try:
        client = openai.OpenAI()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Sakura, a friendly restaurant assistant."},
                {"role": "user", "content": payload.message}
            ],
            temperature=0.7,
            max_tokens=150
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"⚠️ Error: {str(e)}"}
