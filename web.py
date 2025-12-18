# functions.py

# --- User authentication ---
USERS = {
    "amanstrat": "123",      # username : password
    "Limay": "abc123",
    "Hayati": "yatie123",
    "Shana" : "shana123",
    "Noor"  : "noor123",
    "FTAteam" : "fta123",
    "CCD" : "ccd123"
    
}

def validate_user(username, password):
    """Return True if user exists and password matches"""
    return username in USERS and USERS[username] == password


# --- Todo functions ---
def get_todos(username):
    """Read todo list for a specific user"""
    filepath = f"todo_{username}.txt"
    try:
        with open(filepath, 'r') as file_local:
            todos_local = file_local.readlines()
    except FileNotFoundError:
        # Create empty file if not exists
        with open(filepath, 'w') as file_local:
            pass
        todos_local = []
    return todos_local


def write_todos(username, todos_arg):
    """Write todo list for a specific user"""
    filepath = f"todo_{username}.txt"
    with open(filepath, 'w') as file:
        file.writelines(todos_arg)
