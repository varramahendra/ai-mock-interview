from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai import ask_ai
import sqlite3

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Init
conn = sqlite3.connect("interviews.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    answer TEXT,
    feedback TEXT
)
""")

conn.commit()


@app.get("/")
def home():
    return {"message": "AI Mock Interview API Running"}


@app.post("/interview")
async def interview(data: dict):

    answer = data.get("answer")

    if not answer:
        return {"error": "Answer required"}

    reply = ask_ai(answer)

    # Save to DB
    cursor.execute(
        "INSERT INTO history (answer, feedback) VALUES (?, ?)",
        (answer, reply)
    )
    conn.commit()

    return {"reply": reply}


@app.get("/history")
def get_history():

    cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()

    return rows
