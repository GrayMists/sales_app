import streamlit as st





def load_all_profiles(supabase):
    if supabase is None:
        if "supabase" not in st.session_state:
            st.error("❌ Немає підключення до Supabase.")
            return
        supabase = st.session_state.supabase

    try:
        response = supabase.table("profiles").select("*").execute()
        st.write("📦 Відповідь з Supabase:", response)  # <-- Додано
        profiles = response.data
        if profiles:
            st.session_state["all_profiles"] = profiles
            st.success(f"✅ Завантажено профілів: {len(profiles)}")
        else:
            st.warning("⚠️ Список користувачів порожній.")
    except Exception as e:
        st.error("❌ Не вдалося завантажити список користувачів.")
        st.exception(e)

def show_data():

    if "user" in st.session_state:
        user = st.session_state["user"]
        profile = st.session_state["profile"]
        full_name = profile["full_name"]
        email = user.email
        territory = profile["territory"]
    with st.container(border=True):
        st.markdown(
            f"<h3 style='text-align: center;'>👤 {full_name}</h3>"
            f"<h4 style='text-align: center;'>{email}</h4>"
            f"<h4 style='text-align: center;'>{territory}</h4>",
            unsafe_allow_html=True
        )
