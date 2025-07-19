from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

@app.get("/")
def root():
    return {"status": "✅ Gemini Chatbot is running"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")

    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    body = {
        "contents": [
            {
                "parts": [{"text": user_message}]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_URL, params=params, headers=headers, json=body)
        result = response.json()

    try:
        reply = result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        reply = f"❗ Error: {str(e)}"

    return {"response": reply}
