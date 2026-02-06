import requests
import json

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


def ask_ai(answer):

    messages = [
        {
            "role": "system",
            "content": "You are a professional technical interviewer. Be concise."
        },
        {
            "role": "user",
            "content": f"""
Evaluate this answer.

Give:
1. Score (1-10)
2. One strength
3. One weakness
4. One improvement
5. Next question

Max 5 lines.

Answer:
{answer}
"""
        }
    ]

    payload = {
        "model": "phi",
        "messages": messages,
        "stream": False
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(
            OLLAMA_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=300
        )

        res.raise_for_status()

        data = res.json()

        return data["message"]["content"]

    except Exception as e:
        return f"LOCAL_AI_ERROR: {str(e)}"
