# --- Hardcoded users ---
# username:password
USERS = {
    "amanstrat": "12345",
    "user2": "password2"
}

# --- Todo functions ---
import json
import os

def get_todos(username):
    if not username:
        return []
    filepath = f"todos_{username}.txt"
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        return f.readlines()

def write_todos(todos, username):
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as f:
        f.writelines(todos)
