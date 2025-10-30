import os

def get_user_filepath(username):
    """Create a separate file for each user."""
    folder = "user_data"
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"todos_{username}.txt")

def get_todos(username):
    filepath = get_user_filepath(username)
    if not os.path.exists(filepath):
        with open(filepath, 'w') as file:
            pass  # create empty file
    with open(filepath, 'r') as file:
        todos_local = file.readlines()
    return todos_local

def write_todos(todos_arg, username):
    filepath = get_user_filepath(username)
    with open(filepath, 'w') as file:
        file.writelines(todos_arg)
