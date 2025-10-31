import hashlib
import json
import os

USER_FILE = "users.json"

# --- User Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    try:
        with open(USER_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def authenticate(username, password):
    if not username or not password:
        return False
    users = load_users()
    username = username.strip().lower()
    hashed = hash_password(password)
    return users.get(username) == hashed

def register_user(username, password):
    if not username or not password:
        return False
    username = username.strip().lower()
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

# --- Todo Functions ---
def get_todos(username):
    if not username:
        return []
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    try:
        with open(filepath, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def write_todos(todos_arg, username):
    if not username:
        return
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as f:
        f.writelines(todos_arg)
