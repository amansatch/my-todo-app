import streamlit as st
import functions
import json
import uuid
from datetime import date, datetime

# --- Helpers ---
def make_id():
    return str(uuid.uuid4())

def ensure_id(todo):
    if "id" not in todo or not todo["id"]:
        todo["id"] = make_id()

# --- Clean old session ---
for key in ["logged_out", "login_user", "login_pass", "reg_user", "reg_pass"]:
    if key in st.session_state:
        del st.session_state[key]

# --- Login/Register ---
st.sidebar.title("🔐 Account Access")
login_tab, register_tab = st.sidebar.tabs(["Login", "Register"])

with login_tab:
    username_input = st.text_input("Username", key="login_user")
    password_input = st.text_input("Password", type="password", key="login_pass")
    if st.button("🔓 Login"):
        if functions.authenticate(username_input, password_input):
            st.session_state["username"] = username_input.strip().lower()
            st.success(f"Logged in as {st.session_state['username']}")
            st.rerun()
        else:
            st.error("Invalid username or password.")

with register_tab:
    new_user = st.text_input("New Username", key="reg_user")
    new_pass = st.text_input("New Password", type="password", key="reg_pass")
    if st.button("📝 Register"):
        if functions.register_user(new_user, new_pass):
            st.success("✅ User registered successfully! You can now log in.")
        else:
            st.warning("⚠️ Username already exists or invalid input.")

# --- Require login ---
username = st.session_state.get("username")
if not username:
    st.stop()

# --- Logout ---
if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.success("Logged out.")
    st.stop()

# --- Load todos ---
raw_todos = functions.get_todos(username)
todos = []
for t in raw_todos:
    try:
        obj = json.loads(t)
        obj.setdefault("task", str(t).strip())
        obj.setdefault("due", "")
        obj.setdefault("progress", 0)
        ensure_id(obj)
        todos.append(obj)
    except json.JSONDecodeError:
        todos.append({"task": t.strip(), "due": "", "progress": 0, "id": make_id()})

# --- Save todos ---
def save_todos():
    data = [json.dumps(t) + "\n" for t in todos]
    functions.write_todos(data, username)

# --- Add todo ---
def add_todo():
    task = st.session_state.get("new_todo", "").strip()
    due = st.session_state.get("new_due_date")
    if not task or not due:
        st.warning("⚠️ Task and due date required.")
        return
    if due < date.today():
        st.error("⚠️ Due date cannot be past.")
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
    st.rerun()

# --- Delete selected ---
def delete_selected():
    selected_ids = st.session_state.get("selected_delete", [])
    if selected_ids:
        global todos
        todos = [t for t in todos if t["id"] not in set(selected_ids)]
        save_todos()
        st.session_state["selected_delete"] = []
        st.rerun()

# --- Page ---
st.title("Todo Planner")
st.subheader(f"Welcome, {username}")

# --- Display todos ---
st.subheader("Your Tasks")
if todos:
    header_cols = st.columns([0.07, 0.43, 0.25, 0.25])
    header_cols[0].markdown("**Done**")
    header_cols[1].markdown("**Task**")
    header_cols[2].markdown("**Due**")
    header_cols[3].markdown("**Progress**")

    if "selected_delete" not in st.session_state:
        st.session_state["selected_delete"] = []

    for todo in todos:
        ensure_id(todo)
        tid = todo["id"]
        col1, col2, col3, col4 = st.columns([0.07, 0.43, 0.25, 0.25])
        with col1:
            chk = st.checkbox("", key=f"chk_{tid}")
            if chk:
                if tid not in st.session_state["selected_delete"]:
                    st.session_state["selected_delete"].append(tid)
            else:
                if tid in st.session_state["selected_delete"]:
                    st.session_state["selected_delete"].remove(tid)
        with col2:
            todo["task"] = st.text_input("", value=todo.get("task", ""), key=f"task_{tid}", label_visibility="collapsed")
        with col3:
            due_str = ""
            if todo.get("due"):
                due_str = datetime.strptime(todo["due"], "%Y-%m-%d").strftime("%d/%m/%Y")
            entered_due = st.text_input("", value=due_str, key=f"due_{tid}", placeholder="DD/MM/YYYY", label_visibility="collapsed")
            if entered_due.strip():
                try:
                    todo["due"] = datetime.strptime(entered_due.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    st.warning(f"⚠️ Invalid date format for {todo['task']}")
        with col4:
            todo["progress"] = st.slider("", 0, 100, value=int(todo.get("progress", 0)), key=f"prog_{tid}", label_visibility="collapsed")
    st.button("🗑️ Delete Selected", on_click=delete_selected)
else:
    st.info("No tasks yet. Add one below!")

# --- Add new task ---
st.subheader("Add a New Task")
st.text_input("Task Name", key="new_todo")
st.date_input("Due Date", key="new_due_date")
st.button("➕ Add Task", on_click=add_todo)
