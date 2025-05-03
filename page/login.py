import streamlit as st
from supabase import create_client, Client




url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]




# Перевірка чи вже є клієнт у session_state
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(url, key)

# Використовуємо supabase з session_state
supabase = st.session_state.supabase


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
                # Отримуємо профіль користувача
                user_id = user.user.id
                response = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
                
                if response.data:
                    st.session_state["profile"] = response.data
                else:
                    st.warning("Профіль користувача не знайдено.")
                
                st.rerun()
                if "all_profiles" in st.session_state:
                    st.write("🧾 Завантажені профілі:", st.session_state["all_profiles"])
                else:
                    st.warning("ℹ️ all_profiles ще не завантажені.")
            except Exception as e:
                st.error("Login failed")
                st.exception(e)
