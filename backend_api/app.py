from fastapi import FastAPI
from typing import List
import psycopg2
import os

app = FastAPI()

# Database connection parameters
DB_PARAMS = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "database": os.getenv("POSTGRES_DB", "streaming"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "port": 5432,
}

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

# Health check route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Flagged Users API!"}

@app.get("/flagged-users")
def get_flagged_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, reason, flagged_at FROM flagged_users ORDER BY flagged_at DESC LIMIT 50")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [
        {"user_id": row[0], "reason": row[1], "flagged_at": row[2].isoformat()} for row in rows
    ]
