import os
import requests
import json

# Gemini API Key
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"


def ask_ai(answer):

    if not GEMINI_KEY:
        return "ERROR: Gemini API key not found"

    prompt = f"""
You are a professional technical interviewer.

Give:
1. Score (1-10)
2. Strength
3. Weakness
4. Improvement
5. Next question

Answer:
{answer}
"""

    headers = {
        "Content-Type": "application/json"
    }

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
            f"{GEMINI_URL}?key={GEMINI_KEY}",
            headers=headers,
            json=payload,
            timeout=60
        )

        res.raise_for_status()

        data = res.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"GEMINI_ERROR: {str(e)}"
