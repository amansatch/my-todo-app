import os
import json
import uuid

# --- Hardcoded Users ---
# username:password pairs
USERS = {
    "amanstrat": "12345",
    "user2": "password2"
}

# --- User Functions ---
def authenticate(username, password):
    """
    Authenticate hardcoded users.
    """
    if not username or not password:
        return False
    username = username.strip().lower()
    password = password.strip()
    return USERS.get(username) == password

# --- Todo Functions ---
def get_todos(username):
    """
    Load todos from user's file.
    """
    if not username:
        return []
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            todos = []
            for t in lines:
                try:
                    todos.append(json.loads(t))
                except json.JSONDecodeError:
                    todos.append({"task": t.strip(), "due": "", "progress": 0, "id": str(uuid.uuid4())})
            return todos
    except FileNotFoundError:
        return []

def write_todos(todos_arg, username):
    """
    Save todos to user's file.
    """
    if not username:
        return
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as f:
        for t in todos_arg:
            f.write(json.dumps(t) + "\n")
