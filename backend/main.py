import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

# Load API Key from Render Environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini
model = genai.GenerativeModel("gemini-pro")

# Create App
app = FastAPI(title="AI Mock Interview API")


class InterviewRequest(BaseModel):
    role: str
    experience: str
    topic: str


# Health Check
@app.get("/")
def home():
    return {"status": "Server Running"}


# Interview API
@app.post("/interview")
def interview(req: InterviewRequest):
    try:
        prompt = f"""
You are a professional interviewer.

Role: {req.role}
Experience: {req.experience}
Topic: {req.topic}

Ask 5 technical interview questions.
Give feedback.
Be strict.
"""

        response = model.generate_content(prompt)

        return {"result": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
