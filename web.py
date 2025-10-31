import streamlit as st
from datetime import date
import os

# --- Hardcoded Users ---
USERS = {
    "amanstrat": "yngwie11"
}

# --- Sidebar Login ---
st.sidebar.title("🔐 Account Access")

if "username_input" not in st.session_state:
    st.session_state["username_input"] = ""
if "password_input" not in st.session_state:
    st.session_state["password_input"] = ""

username_input = st.sidebar.text_input("Username", key="username_input")
password_input = st.sidebar.text_input("Password", type="password", key="password_input")

if st.sidebar.button("🔓 Login"):
    if username_input in USERS and password_input == USERS[username_input]:
        st.session_state["username"] = username_input
    else:
        st.sidebar.error("Invalid username or password.")

# --- Logout ---
if "username" in st.session_state:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.stop()

# --- Require login ---
if "username" not in st.session_state:
    st.warning("👤 Please log in to continue.")
    st.stop()

username = st.session_state["username"]
st.sidebar.success(f"Logged in as {username}")

# --- Todo Functions ---
def get_todos(username):
    filepath = f"todos_{username}.txt"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def write_todos(todos, username):
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as f:
        for t in todos:
            f.write(t + "\n")

# --- Load Todos ---
todos = get_todos(username)

# --- Save Todos ---
def save_todos():
    write_todos(todos, username)

# --- Add Todo ---
def add_todo():
    task = st.session_state.get("new_todo", "").strip()
    if not task:
        st.warning("⚠️ Please enter a task.")
        return
    todos.append(task)
    save_todos()
    st.session_state["new_todo"] = ""

# --- Delete Selected ---
def delete_selected():
    selected = st.session_state.get("selected_delete", [])
    if selected:
        global todos
        todos = [t for i, t in enumerate(todos) if i not in set(selected)]
        save_todos()
        st.session_state["selected_delete"] = []

# --- Page Title ---
st.markdown("<h1 style='color: teal; text-align: center;'>Todo Planner</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc'>", unsafe_allow_html=True)

# --- Display Todos ---
st.subheader("Your Tasks")
if todos:
    if "selected_delete" not in st.session_state:
        st.session_state["selected_delete"] = []

    for i, task in enumerate(todos):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            chk = st.checkbox("", key=f"chk_{i}")
            if chk:
                if i not in st.session_state["selected_delete"]:
                    st.session_state["selected_delete"].append(i)
            else:
                if i in st.session_state["selected_delete"]:
                    st.session_state["selected_delete"].remove(i)
        with col2:
            st.text(task)

    st.button("🗑️ Delete Selected", on_click=delete_selected)
else:
    st.info("No tasks yet. Add one below!")

# --- Add New Task ---
st.markdown("<hr style='border:1px solid #ccc'>", unsafe_allow_html=True)
st.subheader("Add a New Task")
st.text_input("Task Name", placeholder="Type your task here...", key="new_todo")
st.button("➕ Add Task", on_click=add_todo)
