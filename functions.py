import hashlib
import sqlite3
import os

DB_FILE = "data.db"

# --- Initialize database (run once) ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- User Management ---
def register_user(username, password):
    username = username.strip().lower()
    password = password.strip()

    if not username or not password:
        return False

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE username=?", (username,))
    if cur.fetchone():
        conn.close()
        return False

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password)))
    conn.commit()
    conn.close()
    return True

def authenticate(username, password):
    username = username.strip().lower()
    password = password.strip()

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return False
    return hash_password(password) == row[0]

# --- Todo Management ---
def get_todos(username):
    filepath = f"todos_{username}.txt"
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def write_todos(todos, username):
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as file:
        file.writelines(todos)

# Initialize the database
init_db()
