from flask import Flask, request, redirect, render_template_string
import hashlib
import json
import os

app = Flask(__name__)

USER_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def authenticate(username, password):
    username = username.strip().lower()
    users = load_users()
    hashed = hash_password(password)
    return users.get(username) == hashed

def register_user(username, password):
    username = username.strip().lower()
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    save_users(users)
    return True

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


# ---------------------- ROUTES ----------------------

@app.route("/")
def home():
    return """
    <h1>Todo App</h1>
    <form method='POST' action='/login'>
        <input name='username' placeholder='Username'><br>
        <input name='password' type='password' placeholder='Password'><br>
        <input type='submit' value='Login'>
    </form>
    <form method='POST' action='/register'>
        <input name='username' placeholder='New Username'><br>
        <input name='password' type='password' placeholder='New Password'><br>
        <input type='submit' value='Register'>
    </form>
    """


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if authenticate(username, password):
        return redirect(f"/todos/{username}")
    else:
        return "<p>Invalid username or password</p><a href='/'>Go back</a>"


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    if register_user(username, password):
        return "<p>Registration successful!</p><a href='/'>Go back</a>"
    else:
        return "<p>Username already exists!</p><a href='/'>Go back</a>"


@app.route("/todos/<username>")
def todos(username):
    todos_list = get_todos(username)
    todos_html = "".join(f"<li>{t}</li>" for t in todos_list)
    return f"""
    <h2>{username}'s Todos</h2>
    <ul>{todos_html}</ul>
    <form method='POST' action='/add/{username}'>
        <input name='todo' placeholder='New todo'>
        <input type='submit' value='Add'>
    </form>
    <a href='/'>Logout</a>
    """


@app.route("/add/<username>", methods=["POST"])
def add(username):
    todo = request.form["todo"].strip()
    todos = get_todos(username)
    if todo:
        todos.append(todo + "\n")
        write_todos(todos, username)
    return redirect(f"/todos/{username}")


if __name__ == "__main__":
    app.run(debug=True)
