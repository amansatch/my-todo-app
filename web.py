from flask import Flask, request, redirect, render_template_string, session, url_for
import hashlib
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # change this in production

USER_FILE = "users.json"

# ------------------ Utility functions ------------------

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
        with open(filepath, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def write_todos(todos, username):
    filepath = f"todos_{username}.txt"
    with open(filepath, 'w') as f:
        f.writelines(todos)

# ------------------ HTML templates ------------------

home_page = """
<!DOCTYPE html>
<html>
<head><title>Login or Register</title></head>
<body>
<h2>Login</h2>
<form method="post" action="/login">
  Username: <input name="username"><br>
  Password: <input type="password" name="password"><br>
  <button type="submit">Login</button>
</form>

<h2>Register</h2>
<form method="post" action="/register">
  Username: <input name="username"><br>
  Password: <input type="password" name="password"><br>
  <button type="submit">Register</button>
</form>

<p style="color:red;">{{ message }}</p>
</body>
</html>
"""

todos_page = """
<!DOCTYPE html>
<html>
<head><title>Your To-Dos</title></head>
<body>
<h2>Hello, {{ username }}!</h2>
<form method="post" action="/add">
  <input name="todo" placeholder="New to-do">
  <button type="submit">Add</button>
</form>

<ul>
{% for item in todos %}
  <li>{{ item.strip() }}</li>
{% endfor %}
</ul>

<form method="post" action="/logout">
  <button type="submit">Logout</button>
</form>
</body>
</html>
"""

# ------------------ Routes ------------------

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('todos'))
    return render_template_string(home_page, message="")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if authenticate(username, password):
        session['username'] = username.strip().lower()
        return redirect(url_for('todos'))
    return render_template_string(home_page, message="Invalid login!")

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if register_user(username, password):
        return render_template_string(home_page, message="Registration successful! Please log in.")
    else:
        return render_template_string(home_page, message="Username already exists!")

@app.route('/todos')
def todos():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    todos_list = get_todos(username)
    return render_template_string(todos_page, username=username, todos=todos_list)

@app.route('/add', methods=['POST'])
def add():
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    new_todo = request.form['todo'].strip()
    todos_list = get_todos(username)
    if new_todo:
        todos_list.append(new_todo + "\n")
        write_todos(todos_list, username)
    return redirect(url_for('todos'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect('/')

# ------------------ Run the app ------------------

if __name__ == "__main__":
    # create users file if missing
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    app.run(debug=True)
