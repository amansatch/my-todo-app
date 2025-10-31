import hashlib
import json
import os

USER_FILE = "users.json"

def hash_password(password):
    """Hash the password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load existing users from the JSON file."""
    if not os.path.exists(USER_FILE):
        return {}
    try:
        with open(USER_FILE, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {}
            return data
    except json.JSONDecodeError:
        # If corrupted file, reset it
        return {}

def save_users(users):
    """Save users dictionary to JSON."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def authenticate(username, password):
    """Check if username and password are valid."""
    username = username.strip().lower()
    users = load_users()
    if username not in users:
        return False
    hashed_input = hash_password(password)
    return users[username] == hashed_input

def register_user(username, password):
    """Register a new user if not exists."""
    username = username.strip().lower()
    password = password.strip()

    if not username or not password:
        return False

    users = load_users()
    if username in users:
        return False

    users[username] = hash_password(password)
    save_users(users)
    return True

def get_todos(username):
    """Get todos for specific user."""
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    try:
        with open(filepath, 'r') as file_local:
            todos_local = file_local.readlines()
        return todos_local
    except FileNotFoundError:
        return []

def write_todos(todos_arg, username):
    """Write todos for specific user."""
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    with open(filepath, 'w') as file:
        file.writelines(todos_arg)
