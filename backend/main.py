import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai


# Load Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")


# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Use latest working model
model = genai.GenerativeModel("gemini-1.5-flash")


# Create App
app = FastAPI(title="AI Mock Interview API")


# Enable CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Model (matches frontend)
class InterviewRequest(BaseModel):
    answer: str


# Health Check
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

    try:
        response = model.generate_content(prompt)

        return {"reply": response.text}

    except Exception as e:
        return {"reply": f"GEMINI_ERROR: {str(e)}"}


# History (simple placeholder)
@app.get("/history")
def history():
    return []
