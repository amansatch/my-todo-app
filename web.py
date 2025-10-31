import streamlit as st
import hashlib
import json
import os

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

# --------------------- STREAMLIT UI ---------------------

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("Simple Todo App")

# --- LOGIN & REGISTER PAGE ---
if st.session_state.username == "":
    action = st.radio("Choose action:", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if action == "Login":
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.username = username.strip().lower()
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    else:
        if st.button("Register"):
            if register_user(username, password):
                st.success("Registration successful, please log in.")
            else:
                st.warning("Username already exists.")

# --- TODO PAGE (AFTER LOGIN) ---
else:
    username = st.session_state.username
    st.write(f"Logged in as: **{username}**")

    todos = get_todos(username)

    # Show todos
    st.write("Your Todos:")
    for todo in todos:
        st.write("-", todo.strip())

    # Add todo
    new_todo = st.text_input("New todo:")
    if st.button("Add"):
        if new_todo.strip():
            todos.append(new_todo.strip() + "\n")
            write_todos(todos, username)
            st.experimental_rerun()
        else:
            st.warning("Todo cannot be empty.")

    # Logout button
    if st.button("Logout"):
        st.session_state.username = ""
        st.experimental_rerun()
