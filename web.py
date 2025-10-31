import streamlit as st
import functions
import json
import uuid
from datetime import date, datetime

# --- Hardcoded users ---
# username:password
USERS = {
    "amanstrat": "12345",
    "user2": "password2"
}

# --- Clean leftover flags ---
for key in ["logged_out", "login_user", "login_pass"]:
    if key in st.session_state:
        del st.session_state[key]

# --- Login ---
st.sidebar.title("🔐 Login")
username_input = st.sidebar.text_input("Username", key="login_user")
password_input = st.sidebar.text_input("Password", type="password", key="login_pass")
if st.sidebar.button("Login"):
    if username_input in USERS and USERS[username_input] == password_input:
        st.session_state["username"] = username_input
        st.rerun()
    else:
        st.error("Invalid username or password.")

# --- Require login ---
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

# --- Load todos ---
raw_todos = functions.get_todos(username)
todos = []
for t in raw_todos:
    line = t.strip()
    if line:
        todos.append({"task": line, "due": "", "progress": 0, "id": make_id()})

# --- Save todos ---
def save_todos():
    data = [t["task"] + "\n" for t in todos]
    functions.write_todos(data, username)

# --- Add todo ---
def add_todo():
    task = st.session_state.get("new_todo", "").strip()
    if not task:
        st.warning("⚠️ Please enter a task name.")
        return
    todos.append({"task": task, "due": "", "progress": 0, "id": make_id()})
    save_todos()
    st.session_state["new_todo"] = ""

# --- Delete selected todos ---
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
    header_cols = st.columns([0.07, 0.6, 0.2, 0.1])
    header_cols[0].markdown("**Done**")
    header_cols[1].markdown("**Task**")
    header_cols[2].markdown("**Progress (%)**")
    if "selected_delete" not in st.session_state:
        st.session_state["selected_delete"] = []

    for todo in todos:
        tid = todo["id"]
        col1, col2, col3 = st.columns([0.07, 0.6, 0.2])
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
            progress = st.slider("", 0, 100, value=int(todo.get("progress", 0)), key=f"prog_{tid}", label_visibility="collapsed")
        todo["task"] = task_text.strip()
        todo["progress"] = progress

    st.button("🗑️ Delete Selected", on_click=delete_selected)
    save_todos()
else:
    st.info("No tasks yet. Add one below!")

# --- Add New Task ---
st.markdown("<hr style='border:1px solid #ccc'>", unsafe_allow_html=True)
st
