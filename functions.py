import hashlib
import json
import os

# Use current working directory (always writable on Streamlit Cloud)
BASE_DIR = os.getcwd()
USER_FILE = os.path.join(BASE_DIR, "users.json")


def hash_password(password):
    """Hash password with SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    """Load user data safely."""
    if not os.path.exists(USER_FILE):
        return {}

    try:
        with open(USER_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            data = json.loads(content)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_users(users):
    """Save user data safely."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


def authenticate(username, password):
    """Check login credentials."""
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

    if username in users:
        return False

    users[username] = hash_password(password)
    save_users(users)
    return True


def get_todos(username):
    """Load todos for the specific user."""
    if not username:
        return []
    username = username.strip().lower()
    filepath = os.path.join(BASE_DIR, f"todos_{username}.txt")
    try:
        with open(filepath, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def write_todos(todos, username):
    """Save todos for the specific user."""
    if not username:
        return
    username = username.strip().lower()
    filepath = os.path.join(BASE_DIR, f"todos_{username}.txt")
    with open(filepath, 'w') as f:
        f.writelines(todos)
