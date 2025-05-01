import streamlit as st
from data_cleaner import process_filtered_df




def show_data():
    if "profile" in st.session_state:
        profile = st.session_state["profile"]
        region = profile["region"]
    # Перевірка, чи є дані
    if "df" not in st.session_state:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return
    df = st.session_state.df

    new_df = df[df["Регіон"] == region]
    

    process_filtered_df(new_df,region)


    st.write(new_df)
    

  