import hashlib
import json
import os

# --- Configuration ---
USER_FILE = "users.json"
TODO_DIR = "user_data"

# Ensure user data directory exists
os.makedirs(TODO_DIR, exist_ok=True)


# --- Password Helpers ---
def hash_password(password: str) -> str:
    """Hash password with SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


# --- User Management ---
def load_users() -> dict:
    """Load all registered users."""
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_users(users: dict):
    """Save user database to file."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


def register_user(username: str, password: str) -> bool:
    """Register new user if username not taken."""
    username = username.strip().lower()
    if not username or not password:
        return False

    users = load_users()
    if username in users:
        return False

    users[username] = hash_password(password)
    save_users(users)

    # Create an empty todo file for the user
    filepath = os.path.join(TODO_DIR, f"todos_{username}.txt")
    open(filepath, "a").close()

    return True


def authenticate(username: str, password: str) -> bool:
    """Check username/password match."""
    username = username.strip().lower()
    users = load_users()
    hashed = hash_password(password)
    return users.get(username) == hashed


def delete_user(username: str) -> bool:
    """Optional: Delete a user and their todo file."""
    username = username.strip().lower()
    users = load_users()
    if username not in users:
        return False

    # Remove from user list
    users.pop(username)
    save_users(users)

    # Remove todo file if exists
    filepath = os.path.join(TODO_DIR, f"todos_{username}.txt")
    if os.path.exists(filepath):
        os.remove(filepath)
    return True


# --- Todo Management ---
def get_todos(username: str) -> list:
    """Return todos for specific user."""
    username = username.strip().lower()
    filepath = os.path.join(TODO_DIR, f"todos_{username}.txt")
    try:
        with open(filepath, "r") as file_local:
            return file_local.readlines()
    except FileNotFoundError:
        return []


def write_todos(todos_arg: list, username: str):
    """Save todos for a specific user."""
    username = username.strip().lower()
    filepath = os.path.join(TODO_DIR, f"todos_{username}.txt")
    with open(filepath, "w") as file:
        file.writelines(todos_arg)
