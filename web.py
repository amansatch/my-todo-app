import streamlit as st
import functions
import json
import uuid
from datetime import date, datetime

def make_id():
    return str(uuid.uuid4())

def ensure_id(todo):
    if "id" not in todo or not todo["id"]:
        todo["id"] = make_id()

# --- Load todos ---
raw_todos = functions.get_todos()
todos = []
for t in raw_todos:
    try:
        obj = json.loads(t)
        if "task" not in obj: obj["task"] = str(t).strip()
        if "due" not in obj: obj["due"] = ""
        if "progress" not in obj: obj["progress"] = 0
        ensure_id(obj)
        todos.append(obj)
    except json.JSONDecodeError:
        todos.append({"task": t.strip(), "due": "", "progress": 0, "id": make_id()})

def save_todos():
    data = [json.dumps(t) + "\n" for t in todos]
    functions.write_todos(data)

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
        st.warning("⚠️ The selected due date has already passed.")
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

st.markdown("<h1 style='color: teal; text-align:center;'>Todo Planner</h1>", unsafe_allow_html=True)
st.subheader("Your Tasks")
st.markdown("<p style='text-align:center; color:gray;'>Click checkbox for tasks to delete, then press Delete Selected</p>", unsafe_allow_html=True)

# --- Display todos ---
delete_ids = []
for todo in todos:
    ensure_id(todo)
    tid = todo["id"]
    col1, col2, col3, col4 = st.columns([0.07,0.43,0.25,0.25])
    with col1:
        if st.checkbox("", key=f"chk_{tid}"):
            delete_ids.append(tid)
    with col2:
        todo["task"] = st.text_input("", value=todo.get("task",""), key=f"task_{tid}", label_visibility="collapsed").strip()
    with col3:
        due_str = ""
        if todo.get("due"):
            try:
                due_str = datetime.strptime(todo["due"], "%Y-%m-%d").strftime("%d/%m/%Y")
            except: pass
        entered_due = st.text_input("", value=due_str, key=f"due_{tid}", placeholder="DD/MM/YYYY", label_visibility="collapsed")
        if entered_due.strip():
            try:
                todo["due"] = datetime.strptime(entered_due.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
            except: st.warning("Invalid date format. Use DD/MM/YYYY.")
    with col4:
        todo["progress"] = st.slider("", 0, 100, value=int(todo.get("progress",0)), key=f"prog_{tid}", label_visibility="collapsed")

# --- Delete Selected Button ---
if st.button("🗑️ Delete Selected Tasks"):
    if delete_ids:
        todos = [t for t in todos if t["id"] not in set(delete_ids)]
        save_todos()
        st.success(f"Deleted {len(delete_ids)} task(s).")

# --- Add New Task Section ---
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Add a New Task")
st.text_input("Task Name", placeholder="Type your task here...", key="new_todo")
st.date_input("Select Due Date (DD/MM/YYYY)", key="new_due_date", format="DD/MM/YYYY")
st.button("➕ Add Task", on_click=add_todo)
