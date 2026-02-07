import os
import logging
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv


# ---------------- LOAD ENV ---------------- #

load_dotenv()   # Loads .env file (local only)

logging.basicConfig(level=logging.INFO)


# ---------------- CONFIG ---------------- #

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1/models/"
    "gemini-1.5-flash:generateContent"
)


# ---------------- APP ---------------- #

app = FastAPI(
    title="AI Mock Interview API",
    version="1.0.0"
)


# Enable CORS (for Vercel frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Change later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- MODELS ---------------- #

class InterviewRequest(BaseModel):
    answer: str


class InterviewResponse(BaseModel):
    reply: str


# ---------------- GEMINI CALL ---------------- #

def call_gemini(answer: str) -> str:

    if not GEMINI_API_KEY:
        logging.error("GEMINI_API_KEY missing")
        raise RuntimeError("GEMINI_API_KEY not configured")

    if not answer.strip():
        raise ValueError("Answer is empty")

    prompt = f"""
You are a professional technical interviewer.

Evaluate this answer:

"{answer}"

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

        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=40
        )

        response.raise_for_status()

        data = response.json()

        reply = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text")
        )

        if not reply:
            raise RuntimeError("Empty Gemini response")

        return reply


    except requests.exceptions.Timeout:
        logging.error("Gemini timeout")
        raise RuntimeError("Gemini API timeout")


    except requests.exceptions.RequestException as e:
        logging.error(f"Gemini request failed: {e}")
        raise RuntimeError("Gemini API failed")


    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise


# ---------------- ROUTES ---------------- #

@app.get("/")
def health():

    return {
        "status": "running",
        "gemini_key_loaded": bool(GEMINI_API_KEY)
    }


@app.post("/interview", response_model=InterviewResponse)
def interview(req: InterviewRequest):

    try:

        reply = call_gemini(req.answer)

        return {"reply": reply}


    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


    except RuntimeError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.get("/history")
def history():
    return []
