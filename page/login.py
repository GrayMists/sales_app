import streamlit as st
from supabase import create_client, Client



# Встав свій URL та API ключ із Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(url, key)

def show_login_data():
    st.title("Login with Supabase")

    if "user" not in st.session_state:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        st.file_uploader("Оберіть файл")

        if st.button("Login"):
            try:
                user = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                st.session_state["user"] = user
            except Exception as e:
                st.error("Login failed")
                st.exception(e)

    if "user" in st.session_state and st.session_state["user"] is not None:
        current_user = st.session_state["user"]
        st.subheader("User Profile")

        full_name = current_user.user.user_metadata.get("full_name", "")
        email = current_user.user.email
        st.write("Повне Імʼя:", full_name if full_name else "не вказано")
        st.write("Email:", email)

        if "user_data" not in st.session_state:
            st.session_state.user_data = {
                "email": email,
                "full_name": full_name
            }

        if not full_name:
            with st.form("profile_form"):
                new_full_name = st.text_input("Full Name", value=full_name)
                submitted = st.form_submit_button("Update Profile")
        else:
            with st.expander("Оновити повне імʼя"):
                with st.form("profile_form"):
                    new_full_name = st.text_input("Full Name", value=full_name)
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