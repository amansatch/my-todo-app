import hashlib
import json
import os

# Always use the folder where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_FILE = os.path.join(BASE_DIR, "users.json")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            f.write("{}")
        return {}
    try:
        with open(USER_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

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

def get_todos(username):
    if not username:
        return []
    username = username.strip().lower()
    filepath = os.path.join(BASE_DIR, f"todos_{username}.txt")
    try:
        with open(filepath, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def write_todos(todos, username):
    if not username:
        return
    username = username.strip().lower()
    filepath = os.path.join(BASE_DIR, f"todos_{username}.txt")
    with open(filepath, "w") as f:
        f.writelines(todos)
