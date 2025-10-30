def get_todos(username):
    filepath = f"todos_{username}.txt"
    try:
        with open(filepath, 'r') as file_local:
            todos_local = file_local.readlines()
        return todos_local
    except FileNotFoundError:
        return []

def write_todos(todos_arg, username):
    filepath = f"todos_{username}.txt"
    with open(filepath, 'w') as file:
        file.writelines(todos_arg)
