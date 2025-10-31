import streamlit as st
import functions

st.set_page_config(page_title="My ToDo App", layout="centered")

# --- Session state ---
if "username" not in st.session_state:
    st.session_state.username = None

# --- Login/Register Page ---
if not st.session_state.username:
    st.title("📝 ToDo App Login")

    menu = st.radio("Select option", ["Login", "Register"], horizontal=True)
    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password")

    if menu == "Login":
        if st.button("Login"):
            if functions.authenticate(username, password):
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    else:  # Register
        if st.button("Register"):
            if functions.register_user(username, password):
                st.success("✅ Registration successful! You can now log in.")
            else:
                st.warning("⚠️ Username already exists or invalid input.")

else:
    # --- Main ToDo Page ---
    st.title(f"✅ Welcome, {st.session_state.username}")
    todos = functions.get_todos(st.session_state.username)

    st.subheader("Your Tasks")
    for i, todo in enumerate(todos):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.text(todo.strip())
        with col2:
            if st.button("❌", key=f"del_{i}"):
                todos.pop(i)
                functions.write_todos(todos, st.session_state.username)
                st.rerun()

    st.write("---")
    new_todo = st.text_input("Add new task:")
    if st.button("Add Task"):
        if new_todo.strip():
            todos.append(new_todo + "\n")
            functions.write_todos(todos, st.session_state.username)
            st.success("Task added!")
            st.rerun()
        else:
            st.warning("Please enter a task.")

    st.write("---")
    if st.button("Logout"):
        st.session_state.username = None
        st.rerun()
