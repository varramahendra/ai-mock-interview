import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# Load API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing")


# Gemini REST Endpoint (latest stable)
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1/models/"
    "gemini-1.5-flash:generateContent"
)


# Create App
app = FastAPI(title="AI Mock Interview API")


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Schema
class InterviewRequest(BaseModel):
    answer: str


# Health
@app.get("/")
def home():
    return {"status": "Server Running"}


# Interview API
@app.post("/interview")
def interview(req: InterviewRequest):

    prompt = f"""
You are a professional technical interviewer.

Evaluate this answer:

"{req.answer}"

Give:
1. Score (1-10)
2. Strength
3. Weakness
4. Improvement
5. Next Question
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:

        res = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=60
        )

        res.raise_for_status()

        data = res.json()

        return {
            "reply": data["candidates"][0]["content"]["parts"][0]["text"]
        }

    except Exception as e:
        return {"reply": f"GEMINI_ERROR: {str(e)}"}


# History placeholder
@app.get("/history")
def history():
    return []
