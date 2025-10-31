import hashlib
import json
import os

USER_FILE = "users.json"
TODO_DIR = "user_data"

# Ensure the folder exists
os.makedirs(TODO_DIR, exist_ok=True)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def authenticate(username, password):
    users = load_users()
    hashed = hash_password(password)
    return users.get(username) == hashed

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

def get_todos(username):
    filepath = os.path.join(TODO_DIR, f"todos_{username}.txt")
    try:
        with open(filepath, "r") as file_local:
            return file_local.readlines()
    except FileNotFoundError:
        return []

def write_todos(todos_arg, username):
    filepath = os.path.join(TODO_DIR, f"todos_{username}.txt")
    with open(filepath, "w") as file:
        file.writelines(todos_arg)
