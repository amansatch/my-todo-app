import streamlit as st
import functions
import json
import uuid
from datetime import date, datetime
import io

# --- Helpers ---
def make_id():
    return str(uuid.uuid4())

def ensure_id(todo):
    if "id" not in todo or not todo["id"]:
        todo["id"] = make_id()

# --- User identification ---
# We'll ask each user to enter a username
if "username" not in st.session_state:
    st.session_state["username"] = ""

st.sidebar.header("👤 Your Name")
username = st.sidebar.text_input("Enter your name:", st.session_state["username"])
st.session_state["username"] = username

# File path per user
def get_user_file():
    return f"{username}_todos.txt" if username else "todos.txt"

# --- Load todos ---
raw_todos = functions.get_todos(get_user_file()) if username else []

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
    if username:
        functions.write_todos(data, get_user_file())

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

    # Check if due date already passed
    if due < date.today():
        st.session_state["invalid_due_date"] = True
        return
    else:
        st.session_state["invalid_due_date"] = False

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

if todos:
    header_cols = st.columns([0.07, 0.43, 0.25, 0.25])
    header_cols[0].markdown("**Done**")
    header_cols[1].markdown("**Task**")
    header_cols[2].markdown("**Due Date (DD/MM/YYYY)**")
    header_cols[3].markdown("**Progress (%)**")

    delete_ids = []

    for idx, todo in enumerate(todos):
        ensure_id(todo)
        tid = todo["id"]

        with st.container():
            col1, col2, col3, col4 = st.columns([0.07, 0.43, 0.25, 0.25])

            with col1:
                chk_val = st.checkbox("", key=f"chk_{tid}")

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
                parsed_due = ""
                if entered_due.strip():
                    try:
                        parsed_due = datetime.strptime(entered_due.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
                    except ValueError:
                        st.warning(f"⚠️ Invalid date format in task {idx + 1}. Use DD/MM/YYYY.")
                        parsed_due = todo.get("due", "")

            with col4:
                progress = st.slider(
                    "",
                    0,
                    100,
                    value=int(todo.get("progress", 0)),
                    key=f"prog_{tid}",
                    label_visibility="collapsed"
                )

            todo["task"] = task_text.strip()
            todo["due"] = parsed_due
            todo["progress"] = progress

            if chk_val:
                delete_ids.append(tid)

    if delete_ids:
        todos = [t for t in todos if t["id"] not in set(delete_ids)]
        for tid in delete_ids:
            for k in (f"chk_{tid}", f"task_{tid}", f"due_{tid}", f"prog_{tid}"):
                if k in st.session_state:
                    del st.session_state[k]
        save_todos()
        globals()["todos"] = todos
        st.rerun()

    save_todos()
else:
    st.info("No tasks yet. Add one below!")

# --- Add New Task Section ---
st.markdown("<hr style='border:1px solid #ccc'>", unsafe_allow_html=True)
st.subheader("Add a New Task")

# --- Text Input for Task Name ---
def trigger_date_picker():
    st.session_state["show_date_prompt"] = True

st.text_input(
    label="Task Name",
    placeholder="Type your task here...",
    key="new_todo",
    on_change=trigger_date_picker
)

# --- Show Prompt if user pressed Enter ---
if st.session_state.get("show_date_prompt"):
    st.markdown("🗓️ **Please select a due date below before adding the task.**")
    st.session_state["show_date_prompt"] = False

# --- Date input ---
st.date_input(
    label="Select Due Date (DD/MM/YYYY)",
    key="new_due_date",
    format="DD/MM/YYYY"
)

# --- Show error if invalid date was chosen ---
if st.session_state.get("invalid_due_date"):
    st.error("⚠️ The selected due date has already passed. Please choose a future date.")

# --- Add Task Button ---
st.button("➕ Add Task", on_click=add_todo)

# --- Download current tasks ---
if username and todos:
    todos_json = "\n".join([json.dumps(t) for t in todos])
    st.download_button(
        label="💾 Download My Tasks",
        data=todos_json.encode('utf-8'),
        file_name=f"{username}_todos.txt",
        mime="text/plain"
    )

# --- Upload saved tasks ---
uploaded_file = st.file_uploader("📤 Upload your saved todo file", type=["txt"])
if uploaded_file:
    uploaded_data = uploaded_file.read().decode('utf-8').splitlines()
    todos = [json.loads(line) for line in uploaded_data if line.strip()]
    functions.write_todos(uploaded_data, get_user_file())
    st.success("✅ Your tasks have been loaded!")
    st.rerun()
