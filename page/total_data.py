import streamlit as st
from data_cleaner import process_filtered_df




def show_data():
    # Перевірка наявності даних у сесії
    profile = st.session_state.get("profile")
    if not profile:
        st.warning("Не знайдено профіль користувача.")
        return

    region = profile["region"]

    # Перевірка, чи є дані
    df = st.session_state.get("df")
    if df is None:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return

    # Фільтрація та обробка даних
    filtered_df = df[df["Регіон"] == region]
    filtered_df = process_filtered_df(filtered_df, region)

    mr_df = filtered_df[filtered_df["Територія"] == profile["territory"]]
    st.subheader("Дані по території користувача")
    st.dataframe(mr_df, use_container_width=True, hide_index=True)
    # Виведення таблиці
    st.subheader("Всі дані по регіону")
    st.dataframe(filtered_df)
    

  