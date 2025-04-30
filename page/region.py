import streamlit as st
from sidebar_filter.sidebar import get_selected_region


def show_data():
    # Перевірка, чи є дані
    if "df" not in st.session_state:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return
    df = st.session_state.df

    district_filter = get_selected_region()

    st.write(district_filter)
    st.write(df[df["Регіон"] == district_filter])