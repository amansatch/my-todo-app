# --- Hardcoded users ---
# username:password
USERS = {
    "amanstrat": "yngwie",
    "limay": "limay123"
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

import json
import os

def get_todos(username):
    filepath = f"todos_{username}.json"
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except json.JSONDecodeError:
        return []

def write_todos(todos, username):
    filepath = f"todos_{username}.json"
    try:
        with open(filepath, "w") as f:
            json.dump(todos, f, indent=2)
    except Exception as e:
        print(f"Error writing JSON: {e}")

def write_todos(todos, username):
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as f:
        f.writelines(todos)
