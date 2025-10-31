import streamlit as st
import uuid
from datetime import date
import os

# --- Hardcoded Users ---
USERS = {
    "amanstrat": "yngwie11"
}

# --- Helpers ---
def make_id():
    return str(uuid.uuid4())

# --- Todo Functions ---
def get_todos(username):
    """Return a list of dicts: {'task': ..., 'due': ..., 'progress': ..., 'id': ...}"""
    todos = []
    filepath = f"todos_{username}.txt"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("||")
                task = parts[0]
                due = parts[1] if len(parts) > 1 else ""
                progress = int(parts[2]) if len(parts) > 2 else 0
                tid = parts[3] if len(parts) > 3 else make_id()
                todos.append({"task": task, "due": due, "progress": progress, "id": tid})
    return todos

def write_todos(todos_arg, username):
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as f:
        for t in todos_arg:
            line = f"{t['task']}||{t['due']}||{t['progress']}||{t['id']}\n"
            f.write(line)

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

# --- Sidebar Logout ---
if "username" in st.session_state:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()  # remove all session state
        st.rerun()   # refresh to login screen

# --- Require login ---
if "username" not in st.session_state:
    st.warning("👤 Please log in to continue.")
    st.stop()

username = st.session_state["username"]
st.sidebar.success(f"Logged in as {username}")

# --- Load Todos ---
todos = get_todos(username)

# --- Save Todos ---
def save_todos():
    write_todos(todos, username)

# --- Add Todo ---
def add_todo():
    task = st.session_state.get("new_todo", "").strip()
    due = st.session_state.get("new_due_date")
    if not task:
        st.warning("⚠️ Please enter a task name.")
        return
    if not due:
        st.warning("⚠️ Please select a due date.")
        return
    if due < date.today():
        st.error("⚠️ The selected due date has already passed.")
        return
    todos.append({
        "task": task,
        "due": due.strftime("%Y-%m-%d"),
        "progress": 0,
        "id": make_id()
    })
    save_todos()
    st.session_state["new_todo"] = ""
    st.session_state["new_due_date"] = None

# --- Delete Selected ---
def delete_selected():
    selected_ids = st.session_state.get("selected_delete", [])
    if selected_ids:
        global todos
        todos = [t for t in todos if t["id"] not in set(selected_ids)]
        save_todos()
        st.session_state["selected_delete"] = []

# --- Page Title ---
st.markdown("<h1 style='color: teal; text-align: center;'>Todo Planner</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #ccc'>", unsafe_allow_html=True)

# --- Display Todos ---
st.subheader("Your Tasks")
if todos:
    header_cols = st.columns([0.07, 0.43, 0.25, 0.25])
    header_cols[0].markdown("**Done**")
    header_cols[1].markdown("**Task**")
    header_cols[2].markdown("**Due Date**")
    header_cols[3].markdown("**Progress**")

    if "selected_delete" not in st.session_state:
        st.session_state["selected_delete"] = []

    for todo in todos:
        tid = todo["id"]
        col1, col2, col3, col4 = st.columns([0.07, 0.43, 0.25, 0.25])

        with col1:
            chk_val = st.checkbox("", key=f"chk_{tid}")
            if chk_val:
                if tid not in st.session_state["selected_delete"]:
                    st.session_state["selected_delete"].append(tid)
            else:
                if tid in st.session_state["selected_delete"]:
                    st.session_state["selected_delete"].remove(tid)

        with col2:
            task_text = st.text_input("", value=todo["task"], key=f"task_{tid}", label_visibility="collapsed")

        with col3:
            due_input = st.text_input("", value=todo["due"], key=f"due_{tid}", label_visibility="collapsed")
            todo["due"] = due_input.strip()

        with col4:
            progress = st.slider("", 0, 100, value=todo["progress"], key=f"prog_{tid}", label_visibility="collapsed")
            todo["progress"] = progress

        todo["task"] = task_text.strip()

    st.button("🗑️ Delete Selected", on_click=delete_selected)
    save_todos()
else:
    st.info("No tasks yet. Add one below!")

# --- Add New Task Section ---
st.markdown("<hr style='border:1px solid #ccc'>", unsafe_allow_html=True)
st.subheader("Add a New Task")

def trigger_date_picker():
    st.session_state["show_date_prompt"] = True

st.text_input("Task Name", placeholder="Type your task here...", key="new_todo", on_change=trigger_date_picker)

if st.session_state.get("show_date_prompt"):
    st.markdown("🗓️ **Please select a due date below before adding the task.**")
    st.session_state["show_date_prompt"] = False

st.date_input("Select Due Date", key="new_due_date")
st.button("➕ Add Task", on_click=add_todo)
