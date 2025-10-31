import streamlit as st
import functions
import json
import uuid
from datetime import date, datetime

# --- Sidebar Login ---
st.sidebar.title("🔐 Login")
username = st.sidebar.text_input("Username", key="login_user")
password = st.sidebar.text_input("Password", type="password", key="login_pass")
if st.sidebar.button("🔓 Login"):
    if functions.authenticate(username, password):
        st.session_state["username"] = username.strip().lower()
        st.experimental_rerun()
    else:
        st.sidebar.error("Invalid username or password.")

# --- Require login before showing main app ---
username = st.session_state.get("username")
if not username:
    st.warning("👤 Please log in to continue.")
    st.stop()

# --- Helpers ---
def make_id():
    return str(uuid.uuid4())

def ensure_id(todo):
    if "id" not in todo or not todo["id"]:
        todo["id"] = make_id()

# --- Load todos for this user ---
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
        st.warning("⚠️ Enter task and due date.")
        return
    if due < date.today():
        st.error("⚠️ Due date must be today or later.")
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

# --- Page title ---
st.markdown("<h1 style='color: teal; text-align: center;'>Todo Planner</h1>", unsafe_allow_html=True)

# --- Display todos ---
st.subheader(f"{username}'s Tasks")
if todos:
    for todo in todos:
        ensure_id(todo)
        tid = todo["id"]
        cols = st.columns([0.05, 0.5, 0.25, 0.2])
        with cols[0]:
            chk = st.checkbox("", key=f"chk_{tid}")
        with cols[1]:
            task_text = st.text_input("", value=todo.get("task", ""), key=f"task_{tid}", label_visibility="collapsed")
        with cols[2]:
            due_str = ""
            if todo.get("due"):
                try:
                    due_str = datetime.strptime(todo["due"], "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    pass
            entered_due = st.text_input("", value=due_str, key=f"due_{tid}", label_visibility="collapsed", placeholder="DD/MM/YYYY")
            if entered_due.strip():
                try:
                    parsed_due = datetime.strptime(entered_due.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
                    todo["due"] = parsed_due
                except:
                    st.warning(f"⚠️ Invalid date format for task {todo['task']}.")
        with cols[3]:
            progress = st.slider("", 0, 100, value=int(todo.get("progress", 0)), key=f"prog_{tid}", label_visibility="collapsed")
            todo["progress"] = progress

    st.button("Save Changes", on_click=save_todos)
else:
    st.info("No tasks yet. Add one below!")

# --- Add New Task ---
st.subheader("Add a New Task")
st.text_input("Task Name", key="new_todo")
st.date_input("Due Date", key="new_due_date")
st.button("➕ Add Task", on_click=add_todo)
