import hashlib
import json
import os

USER_FILE = "users.json"

def hash_password(password):
    """Hash password with SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load user data from users.json (safe)."""
    if not os.path.exists(USER_FILE):
        return {}
    try:
        with open(USER_FILE, "r") as f:
            data = json.load(f)
            # Make sure it’s a dictionary
            if isinstance(data, dict):
                return data
            else:
                return {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    """Write user data to file."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def authenticate(username, password):
    """Check username & password."""
    if not username or not password:
        return False
    users = load_users()
    username = username.strip().lower()
    hashed = hash_password(password)
    return users.get(username) == hashed

def register_user(username, password):
    """Register a new user (only if unique)."""
    if not username or not password:
        return False

    username = username.strip().lower()
    users = load_users()

    # Check again after cleaning
    if username in users:
        return False

    users[username] = hash_password(password)
    save_users(users)
    return True

def get_todos(username):
    """Load todos for this user."""
    if not username:
        return []
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    try:
        with open(filepath, 'r') as file_local:
            return file_local.readlines()
    except FileNotFoundError:
        return []

def write_todos(todos_arg, username):
    """Write todos for this user."""
    if not username:
        return
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    with open(filepath, 'w') as file:
        file.writelines(todos_arg)
