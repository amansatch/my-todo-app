import streamlit as st
import os
import uuid
from datetime import date, datetime

# --- Hardcoded user ---
USERNAME = "amanstrat"
PASSWORD = "12345"

# --- Login ---
if "username" not in st.session_state:
    st.subheader("Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    if st.button("Login"):
        if username_input == USERNAME and password_input == PASSWORD:
            st.session_state["username"] = username_input
        else:
            st.error("Invalid username or password")
    st.stop()

username = st.session_state["username"]
st.write(f"Logged in as **{username}**")

# --- Todo helpers ---
def make_id():
    return str(uuid.uuid4())

def get_todos(username):
    filename = f"todos_{username}.txt"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def write_todos(todos, username):
    filename = f"todos_{username}.txt"
    with open(filename, "w") as f:
        for t in todos:
            f.write(t + "\n")

# --- Load todos ---
todos = [{"task": t, "id": make_id()} for t in get_todos(username)]

# --- Display todos ---
st.subheader("Your Tasks")
delete_ids = []
for todo in todos:
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        if st.checkbox("", key=todo["id"]):
            delete_ids.append(todo["id"])
    with col2:
        todo["task"] = st.text_input("", value=todo["task"], key=f"task_{todo['id']}")

# --- Delete selected ---
todos = [t for t in todos if t["id"] not in delete_ids]

# --- Add new task ---
new_task = st.text_input("New Task", key="new_task")
if st.button("Add Task") and new_task.strip():
    todos.append({"task": new_task.strip(), "id": make_id()})

# --- Save todos ---
write_todos([t["task"] for t in todos], username)

# --- Show todos count ---
st.info(f"Total tasks: {len(todos)}")
