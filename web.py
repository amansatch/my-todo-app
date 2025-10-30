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

# --- Load todos ---
raw_todos = functions.get_todos()

todos = []
for t in raw_todos:
    try:
        obj = json.loads(t)
        if "task" not in obj:
            obj["task"] = str(t).strip()
        if "due" not in obj:
            obj["due"] = ""
        if "progress" not in obj:
            obj["progress"] = 0
        ensure_id(obj)
        todos.append(obj)
    except json.JSONDecodeError:
        todos.append({"task": t.strip(), "due": "", "progress": 0, "id": make_id()})

# --- Save todos ---
def save_todos():
    data = [json.dumps(t) + "\n" for t in todos]
    functions.write_todos(data)

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
    st.experimental_rerun()  # safe here after adding

# --- Page Title ---
st.markdown(
    "<h1 style='color: teal; text-align: center; margin-bottom: 0px;'>Todo Planner</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center; color: gray; margin-top: 0px;'>Stay productive and organized!</p>",
    unsafe_allow_html=True
)
st.markdown("<hr style='border:1px solid #ccc'>", unsafe_allow_html=True)

# --- Display Todos ---
st.subheader("Your Tasks")
st.markdown("<p style='text-align: center; color: gray;'>Click checkbox to delete</p>", unsafe_allow_html=True)

delete_ids = []

if todos:
    header_cols = st.columns([0.07, 0.43, 0.25, 0.25])
    header_cols[0].markdown("**Done**")
    header_cols[1].markdown("**Task**")
    header_cols[2].markdown("**Due Date (DD/MM/YYYY)**")
    header_cols[3].markdown("**Progress (%)**")

    for todo in todos:
        ensure_id(todo)
        tid = todo["id"]

        with st.container():
            col1, col2, col3, col4 = st.columns([0.07, 0.43, 0.25, 0.25])

            with col1:
                chk_val = st.checkbox("", key=f"chk_{tid}")
                if chk_val:
                    delete_ids.append(tid)

            with col2:
                task_text = st.text_input(
                    "",
                    value=todo.get("task", ""),
                    key=f"task_{tid}",
                    label_visibility="collapsed"
                )

            with col3:
                due_str = ""
                if todo.get("due"):
                    try:
                        due_date = datetime.strptime(todo["due"], "%Y-%m-%d")
                        due_str = due_date.strftime("%d/%m/%Y")
                    except Exception:
                        due_str = ""
                entered_due = st.text_input(
                    "",
                    value=due_str,
                    key=f"due_{tid}",
                    label_visibility="collapsed",
                    placeholder="DD/MM/YYYY"
                )
                parsed_due = todo.get("due", "")
                if entered_due.strip():
                    try:
                        parsed_due = datetime.strptime(entered_due.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
                    except ValueError:
                        st.warning(f"⚠️ Invalid date format in task '{task_text}'. Use DD/MM/YYYY.")

            with col4:
                progress = st.slider(
                    "",
                    0,
                    100,
                    value=int(todo.get("progress", 0)),
                    key=f"prog_{tid}",
                    label_visibility="collapsed"
                )

            # Save updated values
            todo["task"] = task_text.strip()
            todo["due"] = parsed_due
            todo["progress"] = progress

# --- Delete Button ---
if delete_ids:
    if st.button("🗑️ Delete Selected Tasks"):
        todos = [t for t in todos if t["id"] not in set(delete_ids)]
        # Clear session_state keys for deleted todos
        for tid in delete_ids:
            for k in (f"chk_{tid}", f"task_{tid}", f"due_{tid}", f"prog_{tid}"):
                if k in st.session_state:
                    del st.session_state[k]
        save_todos()
        st.experimental_rerun()  # Refresh page automatically after deletion

# --- Add New Task Section ---
st.markdown("<hr style='border:1px solid #ccc'>", unsafe_allow_html=True)
st.subheader("Add a New Task")

st.text_input(
    label="Task Name",
    placeholder="Type your task here...",
    key="new_todo"
)

st.date_input(
    label="Select Due Date (DD/MM/YYYY)",
    key="new_due_date",
    format="DD/MM/YYYY"
)

st.button("➕ Add Task", on_click=add_todo)
