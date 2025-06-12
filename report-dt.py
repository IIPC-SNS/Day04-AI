import streamlit as st
import requests

# --- Configuration ---
WEBHOOK_URL = "https://dterp.app.n8n.cloud/webhook-test/896e1e26-0446-45ce-960f-792b3704e6b6"

# Dummy credentials (username: admin, password: secret)
VALID_USERS = {
    "admin": "admin",
    "alice": "secret"
}

# --- Session State Helper ---
def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

# --- Login Functionality ---
def login():
    st.title("Employee Portal Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")

# --- Main App Form ---
def main_app():
    st.title("Meeting Action Items Form")

    st.markdown(f"👤 Logged in as **{st.session_state.username}**")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

    st.subheader("Submit a new action item")

    with st.form("action_item_form"):
        meeting_title = st.text_input("Meeting Title")
        action_item = st.text_area("Action Item Description")
        assigned_to = st.text_input("Assigned To")
        email = st.text_input("Email")  # Added email field
        due_date = st.date_input("Due Date")

        submitted = st.form_submit_button("Submit")

        if submitted:
            data = {
                "username": st.session_state.username,
                "meeting_title": meeting_title,
                "action_item": action_item,
                "assigned_to": assigned_to,
                "email": email,
                "due_date": str(due_date)
            }

            try:
                response = requests.post(WEBHOOK_URL, json=data)
                if response.status_code == 200:
                    st.success("Action item submitted successfully!")
                else:
                    st.error(f"Failed to submit. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- App Flow ---
def main():
    init_session_state()

    if st.session_state.logged_in:
        main_app()
    else:
        login()

if __name__ == "__main__":
    main()
