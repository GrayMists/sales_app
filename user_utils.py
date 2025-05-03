import streamlit as st
import pandas as pd
from page.login import init_supabase





def get_users_profile():
    supabase = init_supabase()
    response = supabase.table("profiles").select("*").execute()
    user_df = pd.DataFrame(response.data)
    return user_df

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
