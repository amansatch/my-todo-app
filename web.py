import streamlit as st
import functions
from datetime import datetime, date

# --- PAGE CONFIG ---
st.set_page_config(page_title="My Todo App", page_icon="✅", layout="centered")

# --- STYLE ---
st.markdown("""
    <style>
    .block-container {padding-top: 2rem;}
    h1, h2, h3 {color: #2E8B57;}
    .stTextInput > div > input {
        border: 1px solid #2E8B57;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .stSlider > div {
        padding-top: 0.1rem; /* moved slider slightly upward */
    }
    .stButton > button {
        background-color: #2E8B57;
        color: white;
        border-radius: 5px;
        padding: 0.4rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.title("🔐 Welcome to Team Todo App")
    st.write("Please login to manage your Team to-do list.")

    username = st.text_input("👤 Username", placeholder="Enter your username", key="login_user")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter your password", key="login_pass")

    if st.button("Login"):
        if functions.validate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Invalid username or password. Try again.")

else:
    # --- MAIN APP ---
    username = st.session_state.username
    todos = functions.get_todos(username)

    st.title(f"My Todo App — {username.capitalize()}")
    st.caption(f"Logged in as **{username}** | {datetime.now().strftime('%A, %d %B %Y')}")

    st.divider()
    st.subheader("📝 Your Tasks")

    # --- Prepare stored tasks ---
    task_data = []
    for t in todos:
        try:
            text, due, progress = t.strip().split("|")
            task_data.append({"task": text, "due": due, "progress": int(progress)})
        except ValueError:
            task_data.append({"task": t.strip(), "due": "-", "progress": 0})

    # --- Reset checkbox selections before rebuild ---
    st.session_state["selected_delete"] = []

    updated_tasks = []

    if task_data:
        # --- Header Row ---
        header = st.columns([0.5, 2.5, 1.5, 2.5, 0.5])
        header[0].markdown("**✔️**")
        header[1].markdown("**Task**")
        header[2].markdown("**Due Date**")
        header[3].markdown("**Progress (%)**")
        header[4].markdown("")

        # --- Task Rows ---
        for i, item in enumerate(task_data):
            # make unique key by adding row index
            tid = f"{username}_{item['task']}_{i}"

            col1, col2, col3, col4, col5 = st.columns([0.5, 2.5, 1.5, 2.5, 0.5])
            with col1:
                mark = st.checkbox("", key=f"chk_{tid}")
                if mark:
                    st.session_state["selected_delete"].append(i)
            with col2:
                st.text(item["task"])
            with col3:
                st.markdown(f"**{item['due']}**")
            with col4:
                new_progress = st.slider("", 0, 100, item["progress"], key=f"prog_{tid}")
            with col5:
                st.write("")

            updated_tasks.append({
                "task": item["task"],
                "due": item["due"],
                "progress": new_progress
            })

        # --- Delete selected tasks ---
        if st.button("✔️ Mark as Done"):
            updated_tasks = [t for idx, t in enumerate(updated_tasks) if idx not in st.session_state["selected_delete"]]
            st.session_state["selected_delete"] = []
            todos = [f"{t['task']}|{t['due']}|{t['progress']}\n" for t in updated_tasks]
            functions.write_todos(username, todos)

            # Clear old checkbox states
            for key in list(st.session_state.keys()):
                if key.startswith(f"chk_{username}_"):
                    del st.session_state[key]

            st.success("Selected tasks marked as done!")
            st.rerun()

        # --- Save all updates ---
        todos = [f"{t['task']}|{t['due']}|{t['progress']}\n" for t in updated_tasks]
        functions.write_todos(username, todos)
    else:
        st.info("No tasks yet. Add your first to-do below! 👇")

    st.divider()
    st.subheader("✏️ Add New Task")

    # --- Add new task ---
    new_task = st.text_input("Task name", placeholder="Enter new task...", key="new_todo")
    new_due = st.date_input("Due date", value=date.today(), format="DD/MM/YYYY", key="new_due")

    if st.button("Add Task ✔️"):
        if new_task.strip():
            todos.append(f"{new_task.strip()}|{new_due.strftime('%d/%m/%Y')}|0\n")
            functions.write_todos(username, todos)
            st.success("Task added successfully!")
            st.rerun()
        else:
            st.warning("Please enter a task name.")

    st.divider()

    # --- FOOTER ---
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.success("Logged out successfully!")
            st.rerun()
    with col2:
        st.markdown(
            "<p style='text-align:right;color:gray;'>Built using Streamlit</p>",
            unsafe_allow_html=True
        )
