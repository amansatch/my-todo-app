import hashlib
import json
import os

# --- TEMPORARY HARDCODED USERS ---
HARDCODED_USERS = {
    "testuser": "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9a6e1f3f0f7"  # password: 12345
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    # Ignore JSON, return hardcoded users
    return HARDCODED_USERS

def save_users(users):
    # Do nothing, since we're using hardcoded users
    pass

def authenticate(username, password):
    if not username or not password:
        return False
    username = username.strip().lower()
    hashed = hash_password(password)
    users = load_users()
    return users.get(username) == hashed

def register_user(username, password):
    # Disable registration temporarily
    return False

# Todos functions remain the same
def get_todos(username):
    if not username:
        return []
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    try:
        with open(filepath, 'r') as file_local:
            return file_local.readlines()
    except FileNotFoundError:
        return []

def write_todos(todos_list, username):
    if not username:
        return
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    with open(filepath, 'w') as file:
        file.writelines(todos_list)
