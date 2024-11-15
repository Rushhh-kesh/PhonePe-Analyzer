# auth.py
import streamlit as st

USER_CREDENTIALS = {
    "FroTest": "FroTest123",
    "ForRushi": "ForRushi",
    "ForFriends": "ForFriends123"
}

def login():
    """Login page for user authentication."""
    st.title("🔒 Login Page")
    username = st.text_input("Enter your Username")
    password = st.text_input("Enter your Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username in USER_CREDENTIALS and password == USER_CREDENTIALS[username]:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password. Please try again.")

def logout():
    """Logout function."""
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
