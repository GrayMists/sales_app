import streamlit as st


if "supabase" in st.session_state:
    supabase = st.session_state.supabase
else:
    st.error("Підключення до Supabase відсутнє. Будь ласка, увійдіть знову.")
    st.stop()  # Зупиняє виконання коду, якщо немає підключення


def show_data():

    if "user" in st.session_state:
        user = st.session_state["user"]
        full_name = user.user_metadata.get("full_name", "Користувач")
        email = user.email
        profile = st.session_state["profile"]
        territory = profile["territory"]
    with st.container(border=True):
        st.markdown(
            f"<h3 style='text-align: center;'>👤 {full_name}</h3>"
            f"<h4 style='text-align: center;'>{email}</h4>"
            f"<h4 style='text-align: center;'>{territory}</h4>",
            unsafe_allow_html=True
        )
