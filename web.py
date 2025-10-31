import streamlit as st
import functions

# --- Login ---
st.sidebar.title("🔐 Login")
username_input = st.sidebar.text_input("Username")
password_input = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Login"):
    if username_input in functions.USERS and functions.USERS[username_input] == password_input:
        st.session_state["username"] = username_input
        st.rerun()
    else:
        st.error("Invalid username or password.")

# --- Require login ---
username = st.session_state.get("username")
if not username:
    st.warning("👤 Please log in to continue.")
    st.stop()

st.write(f"✅ Logged in as {username}")

# --- Load todos ---
raw_todos = functions.get_todos(username)
todos = []
for t in raw_todos:
    line = t.strip()
    if line:
        todos.append({"task": line, "id": line})

# Display todos
for todo in todos:
    st.write(todo["task"])
