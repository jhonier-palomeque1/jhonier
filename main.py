import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Message(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Servidor en la nube ✅"}

@app.post("/chat")  # ✅ ESTE ENDPOINT ES IMPORTANTE
def chat(message: Message):
    try:
        print(f"Mensaje recibido: {message.text}")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system", 
                    "content": "Eres un asistente virtual amable."
                },
                {"role": "user", "content": message.text}
            ],
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        data = response.json()

        choices = data.get("choices")
        if choices and len(choices) > 0:
            ai_text = choices[0].get("message", {}).get("content", "")
            if ai_text:
                return {"reply": ai_text.strip()}

        return {"error": "La IA no devolvió contenido"}

    except Exception as e:
        return {"error": str(e)}