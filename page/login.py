import streamlit as st
from supabase import create_client, Client



# Встав свій URL та API ключ із Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(url, key)

def show_login_data():
    st.title("Login with Supabase")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.success(f"Logged in as: {user.user.email}")
            st.write("Email:", user.user.email)
            st.write("ID:", user.user.id)
            st.write("Created at:", user.user.created_at)
            st.write("Last sign-in at:", user.user.last_sign_in_at)
            st.write("Повне Імʼя:", user.user.user_metadata.get("full_name", ""))
            st.session_state["user"] = user
        except Exception as e:
            st.error("Login failed")
            st.exception(e)

    if "user" in st.session_state:
        current_user = st.session_state["user"]
        st.subheader("User Profile")

        if "user_data" not in st.session_state:
            st.session_state.user_data = {
                "email": current_user.user.email,
                "full_name": current_user.user.user_metadata.get("full_name", "")
            }

        with st.form("profile_form"):
            new_full_name = st.text_input("Full Name", value=st.session_state.user_data["full_name"])
            submitted = st.form_submit_button("Update Profile")

            if submitted:
                try:
                    supabase.auth.update_user({
                        "data": {
                            "full_name": new_full_name
                        }
                    })
                    st.success("Profile updated!")
                    st.session_state.user_data["full_name"] = new_full_name
                except Exception as e:
                    st.error("Update failed")
                    st.exception(e)