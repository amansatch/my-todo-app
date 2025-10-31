import streamlit as st
import hashlib
import json
import os

USER_FILE = "users.json"

# ---------- Utility functions ----------

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
        with open(filepath, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def write_todos(todos, username):
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as f:
        f.writelines(todos)

# ---------- Streamlit UI ----------

st.set_page_config(page_title="My To-Do App", page_icon="📝")

# Initialize session state
if "username" not in st.session_state:
    st.session_state.username = None

st.title("📝 Simple To-Do App")

# ---------- Logged-in view ----------
if st.session_state.username:
    username = st.session_state.username
    st.success(f"Welcome, **{username}**!")

    todos = get_todos(username)

    # Display todos with delete buttons
    st.subheader("Your To-Dos")
    if not todos:
        st.info("No todos yet — add one below!")
    else:
        for i, todo in enumerate(todos):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.write(f"{i+1}. {todo.strip()}")
            with col2:
                if st.button("❌", key=f"del_{i}"):
                    todos.pop(i)
                    write_todos(todos, username)
                    st.experimental_rerun()

    # Add new todo
    new_todo = st.text_input("Add a new task:")
    if st.button("Add"):
        if new_todo.strip():
            todos.append(new_todo.strip() + "\n")
            write_todos(todos, username)
            st.success("Added!")
            st.experimental_rerun()
        else:
            st.warning("Please type something first.")

    # Logout
    if st.button("Logout"):
        st.session_state.username = None
        st.experimental_rerun()

# ---------- Login / Register view ----------
else:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.username = username.strip().lower()
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Register")
        new_user = st.text_input("Choose username", key="reg_user")
        new_pass = st.text_input("Choose password", type="password", key="reg_pass")
        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Registration successful! You can now log in.")
            else:
                st.error("Username already exists — please choose another.")
