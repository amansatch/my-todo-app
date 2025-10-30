import os

def get_todos(username, basepath="data"):
    os.makedirs(basepath, exist_ok=True)
    filepath = os.path.join(basepath, f"{username}.txt")

    if not os.path.exists(filepath):
        open(filepath, 'w').close()

    with open(filepath, 'r') as file:
        todos_local = file.readlines()
    return todos_local


def write_todos(todos_arg, username, basepath="data"):
    os.makedirs(basepath, exist_ok=True)
    filepath = os.path.join(basepath, f"{username}.txt")

    with open(filepath, 'w') as file:
        file.writelines(todos_arg)
