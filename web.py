import os
from datetime import datetime

# --- Todo Functions (TXT only) ---
def get_todos(username):
    """Load todos for this user from a text file (simple)."""
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    todos = []
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                parts = line.strip().split("|")  # task|due|progress
                if len(parts) == 3:
                    task, due, progress = parts
                    try:
                        progress = int(progress)
                    except ValueError:
                        progress = 0
                    todos.append({"task": task, "due": due, "progress": progress, "id": ""})
                else:
                    # fallback if line malformed
                    todos.append({"task": line.strip(), "due": "", "progress": 0, "id": ""})
    return todos

def write_todos(todos, username):
    """Save todos to a text file (simple)."""
    username = username.strip().lower()
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as f:
        for t in todos:
            # Save as: task|due|progress
            f.write(f"{t['task']}|{t.get('due','')}|{t.get('progress',0)}\n")
