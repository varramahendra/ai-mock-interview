import os
import requests
import json

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


def ask_ai(answer):

    prompt = f"""
You are a professional interviewer.

Give:
1. Score (1-10)
2. One strength
3. One weakness
4. One improvement
5. Next question

Answer:
{answer}
"""

    # ---------- CLOUD MODE ----------
    if OPENAI_KEY:

        headers = {
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an interviewer."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            res = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            res.raise_for_status()

            return res.json()["choices"][0]["message"]["content"]

        except Exception as e:
            return f"CLOUD_AI_ERROR: {str(e)}"


    # ---------- LOCAL MODE ----------
    else:

        payload = {
            "model": "phi",
            "messages": [
                {"role": "system", "content": "You are an interviewer."},
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }

        try:

            res = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=180
            )

            res.raise_for_status()

            return res.json()["message"]["content"]

        except Exception as e:
            return f"LOCAL_AI_ERROR: {str(e)}"
