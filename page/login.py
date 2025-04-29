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
        except Exception as e:
            st.error("Login failed")
            st.exception(e)