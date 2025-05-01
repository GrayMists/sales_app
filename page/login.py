import streamlit as st
from supabase import create_client, Client




url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(url, key)

def show_login_data():
    st.title("Увійдіть у свій аккаунт")

    if "user" not in st.session_state:
        email = st.text_input("Електронна пошта")
        password = st.text_input("Пароль", type="password")


        if st.button("Увійти"):
            try:
                user = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                st.session_state["user"] = user.user
                st.rerun()
            except Exception as e:
                st.error("Login failed")
                st.exception(e)

