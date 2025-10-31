import streamlit as st
import json
import uuid
from datetime import date, datetime
import os

# --- Hardcoded Users ---
USERS = {
    "amanstrat": "12345"  # password is 12345
}

# --- Clean up any leftover flags ---
for key in ["logged_out", "login_user", "login_pass", "reg_user", "reg_pass"]:
    if key in st.session_state:
        del st.session_state[key]

# --- Login & Registration Sidebar ---
st.sidebar.title("🔐 Account Access")
login_tab, register_tab = st.sidebar.tabs(["Login", "Register"])

with login_tab:
    username_input = st.text_input("Username", key="login_user")
    password_input = st.text_input("Password", type="password", key="login_pass")
    if st.button("🔓 Login"):
        if username_input in USERS and password_input == USERS[username_input]:
            st.session_state["username"] = username_input
        else:
            st.error("Invalid username or password.")

with register_tab:
    st.info("⚠️ Registration disabled. Only admin can create users.")

# --- Logout ---
if "username" in st.session_state:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.success("You have been logged out.")
        st.stop()

# --- Require login ---
if "username" not in st.session_state:
    st.warning("👤 Please log in to continue.")
    st.stop()

username = st.session_state["username"]
st.sidebar.success(f"Logged in as {username}")

# --- Helpers ---
def make_id():
    return str(uuid.uuid4())

def ensure_id(todo):
    if "id" not in todo or not todo["id"]:
        todo["id"] = make_id()

# --- Todo Functions ---
def get_todos(username):
    filepath = f"todos_{username}.txt"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def write_todos(todos_arg, username):
    filepath = f"todos_{username}.txt"
    with open(filepath, "w") as f:
        for t in todos_arg:
            f.write(t + "\n")

# --- Load todos ---
raw_todos = get_todos(username)
todos = []
for t in raw_todos:
    try:
        obj = json.loads(t)
        obj.setdefault("task", str(t).strip())
        obj.setdefault("due", "")
        obj.setdefault("progress", 0)
        ensure_id(obj)
        todos.append(obj)
    except (json.JSONDecodeError, TypeError):
        todos.append({"task": t.strip(), "due": "", "progress": 0, "id": make_id()})

# --- Save todos ---
def save_todos():
    data = [json.dumps(t) + "\n" for t in todos]
    write_todos([t["task"] for t in todos], username)

# --- Add todo ---
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
        st.error("⚠️ The selected due date has already passed. Please choose a future date.")
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

# --- Delete selected todos ---
def delete_selected():
    selected_ids = st.session_state.get("selected_delete", [])
    if selected_ids:
        global todos
        todos = [t for t in todos if t["id"] not in set(selected_ids)]
        save_todos()
        st.session_state["selected_delete"] = []

# --- Page Title ---
st.markdown(
    "<h1 style='color: teal; text-align: center; margin-bottom: 0px;'>Todo Planner</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: gray; margin-top: 0px;'>Stay productive and organized.</p>",
    unsafe_allow_html=True
)
st.markdown("<hr style='border:1px solid #ccc'>", unsafe_allow_html=True)

# --- Display Todos ---
st.subheader("Your Tasks")
if todos:
    header_cols = st.columns([0.07, 0.43, 0.25, 0.25])
    header_cols[0].markdown("**Done**")
    header_cols[1].markdown("**Task**")
    header_cols[2].markdown("**Due Date (DD/MM/YYYY)**")
    header_cols[3].markdown("**Progress (%)**")

    if "selected_delete" not in st.session_state:
        st.session_state["selected_delete"] = []

    for todo in todos:
        ensure_id(todo)
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
            task_text = st.text_input("", value=todo.get("task", ""), key=f"task_{tid}", label_visibility="collapsed")

        with col3:
            due_str = ""
            if todo.get("due"):
                try:
                    due_date = datetime.strptime(todo["due"], "%Y-%m-%d")
                    due_str = due_date.strftime("%d/%m/%Y")
                except Exception:
                    due_str = ""
            entered_due = st.text_input("", value=due_str, key=f"due_{tid}", label_visibility="collapsed", placeholder="DD/MM/YYYY")
            parsed_due = ""
            if entered_due.strip():
                try:
                    parsed_due = datetime.strptime(entered_due.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    st.warning(f"⚠️ Invalid date format in task {todo['task']}. Use DD/MM/YYYY.")
                    parsed_due = todo.get("due", "")

        with col4:
            progress = st.slider("", 0, 100, value=int(todo.get("progress", 0)), key=f"prog_{tid}", label_visibility="collapsed")

        todo["task"] = task_text.strip()
        todo["due"] = parsed_due
        todo["progress"] = progress

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

st.date_input("Select Due Date (DD/MM/YYYY)", key="new_due_date", format="DD/MM/YYYY")
st.button("➕ Add Task", on_click=add_todo)
