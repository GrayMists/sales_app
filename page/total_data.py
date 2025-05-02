import streamlit as st
from data_cleaner import process_filtered_df
from sidebar_filter.sidebar import selected_region_med_rep




def show_data():
    # Перевірка наявності даних у сесії
    profile = st.session_state.get("profile")
    if not profile:
        st.warning("Не знайдено профіль користувача.")
        return

    region = profile.get("region")
    line = profile.get("line")
    type = profile.get("type")
    city = profile.get("city")

    # Перевірка, чи є дані
    df = st.session_state.get("df")
    if df is None:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return
    
    filtered_df = process_filtered_df(df, region, city)

    if type != "admin":
        # Фільтрація та обробка даних
        mr_df = filtered_df[
            (filtered_df["Територія"] == profile["territory"])&
            (filtered_df["Лінія"] == profile["line"])
            ]
        st.session_state["mr_df"] = mr_df
        st.subheader("Дані по території користувача")
        group_by_product = mr_df.groupby("Найменування")["Кількість"].sum().reset_index()
        group_by_city = mr_df.groupby("Місто")["Кількість"].sum().reset_index()
        col1, col2, col3 = st.columns([2,2,3])

        with col1:
            with st.expander("Загальні продажі в населених пунктах",icon="⬇️"):
                st.dataframe(group_by_city, use_container_width=True, hide_index=True)
        with col2:
            with st.expander("Загальні по продуктах",icon="⬇️"):
                st.dataframe(group_by_product, use_container_width=True, hide_index=True)
        with col3:
            unique_city = selected_region_med_rep()
            group_by_city_product = mr_df[mr_df["Місто"] == unique_city].groupby(["Місто", "Найменування"])["Кількість"].sum().reset_index()  
            with st.expander("Продажі у вибраному населеному пункті(в боковій панелі)",icon="⬇️"):
                st.dataframe(group_by_city_product, use_container_width=True, hide_index=True)
        # Виведення таблиці
        with st.expander("Не розприділені дані"):
            st.dataframe(filtered_df[~filtered_df["Територія"].isin(["Територія 1", "Територія 2"])])
        with st.expander("Всі дані по регіону"):
            st.dataframe(filtered_df)
    else:
        st.subheader("Всі дані по регіону")
        st.dataframe(filtered_df)