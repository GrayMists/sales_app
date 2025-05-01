import streamlit as st
from data_cleaner import process_filtered_df




def show_data():
    # Перевірка наявності даних у сесії
    profile = st.session_state.get("profile")
    if not profile:
        st.warning("Не знайдено профіль користувача.")
        return

    region = profile.get["region"]
    line = profile.get["line"]

    # Перевірка, чи є дані
    df = st.session_state.get("df")
    if df is None:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return

    # Фільтрація та обробка даних
    filtered_df = process_filtered_df(filtered_df, region)

    mr_df = filtered_df[
        (filtered_df["Територія"] == profile["territory"])&
        (filtered_df["Лінія"] == profile["line"])
         ]
    st.subheader("Дані по території користувача")
    group_by_product = mr_df.groupby("Найменвання")["Кількість"].sum().reset_index()
    col1, col2, = st.columns([2,4])

    with col1:
        st.dataframe(group_by_product, use_container_width=True, hide_index=True)
    with col2:   
        st.dataframe(mr_df, use_container_width=True, hide_index=True)
    # Виведення таблиці
    st.subheader("Всі дані по регіону")
    st.dataframe(filtered_df)
    

  