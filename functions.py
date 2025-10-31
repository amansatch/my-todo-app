import sqlite3
import hashlib
import os
import json

DB_FILE = "data.db"

# --- Helper: ensure DB exists ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    # Create users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    # Create todos table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            task TEXT NOT NULL,
            due TEXT,
            progress INTEGER DEFAULT 0,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)
    conn.commit()
    conn.close()

init_db()  # initialize database on import


# --- Password helpers ---
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# --- User Management ---
def register_user(username: str, password: str) -> bool:
    username = username.strip().lower()
    if not username or not password:
        return False

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE username=?", (username,))
    if cur.fetchone():
        conn.close()
        return False  # already exists

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password)))
    conn.commit()
    conn.close()
    return True


def authenticate(username: str, password: str) -> bool:
    username = username.strip().lower()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return False
    return hash_password(password) == row[0]


# --- Todo Management ---
def get_todos(username: str) -> list:
    username = username.strip().lower()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, task, due, progress FROM todos WHERE username=? ORDER BY id", (username,))
    rows = cur.fetchall()
    conn.close()

    todos = []
    for r in rows:
        todos.append(json.dumps({
            "id": r[0],
            "task": r[1],
            "due": r[2] or "",
            "progress": r[3] or 0
        }))
    return [t + "\n" for t in todos]


def write_todos(todos_arg: list, username: str):
    """Overwrite user's todos in the database."""
    username = username.strip().lower()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Clear existing todos
    cur.execute("DELETE FROM todos WHERE username=?", (username,))

    # Insert new todos
    for line in todos_arg:
        try:
            data = json.loads(line.strip())
            cur.execute(
                "INSERT INTO todos (username, task, due, progress) VALUES (?, ?, ?, ?)",
                (username, data.get("task", ""), data.get("due", ""), int(data.get("progress", 0)))
            )
        except Exception:
            continue

    conn.commit()
    conn.close()
