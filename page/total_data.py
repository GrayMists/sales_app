import streamlit as st
import pandas as pd
from data_cleaner import process_filtered_df




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
    full_name = profile.get("full_name")

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
        st.subheader(f"Дані по території користувача {full_name}")
        group_by_product = mr_df.groupby("Найменування")["Кількість"].sum().reset_index()
        group_by_city = mr_df.groupby("Місто")["Кількість"].sum().reset_index()
        col1, col2 = st.columns([2,5])

        with col1:
            st.markdown("""
              ##### Загальні продажі
            """)
            st.dataframe(group_by_product, use_container_width=True, hide_index=True, height=(len(group_by_product) * 36))

        with col2:
            col3, col4 = st.columns(2)
            
            with col3:
                st.markdown("""
                ##### ТОП-5 найкращих
                """)
                st.dataframe(group_by_product.sort_values(by = "Кількість", ascending=False).head(5),  hide_index=True)

                st.markdown("""
                ##### ТОП-5 найгірших
                """)
                st.dataframe(group_by_product.sort_values(by = "Кількість", ascending=True).head(5),  hide_index=True)

                    
            with col4:
                st.markdown("""##### Продажі в населених пунктах""")
                st.dataframe(group_by_city, use_container_width=True, hide_index=True, height=487)
                
            with st.expander("Продажі у вибраному населеному пункті",icon="⬇️"):
                unique_city = st.selectbox('Оберіть населений пункт',mr_df["Місто"].unique(),key='select_city')
                group_by_city_product = mr_df[mr_df["Місто"] == unique_city].groupby(["Місто", "Найменування"])["Кількість"].sum().reset_index()
                st.dataframe(group_by_city_product, use_container_width=True, hide_index=True)
            with st.expander("Продажі у вибраному населеному пункті по вулицях",icon="⬇️"):
                unique_city_street = st.selectbox('Оберіть населений пункт',mr_df["Місто"].unique(),key='select_city_streer')
                filtered_streets = mr_df[mr_df["Місто"] == unique_city_street]["Вулиця"].unique()

                unique_street = st.selectbox('Оберіть вулицю',filtered_streets,key='select_streer')
                group_by_street_product = mr_df[(mr_df["Місто"] == unique_city_street) & (mr_df["Вулиця"] == unique_street)].groupby(["Місто","Вулиця", "Найменування"])["Кількість"].sum().reset_index()
                st.dataframe(group_by_street_product.drop(columns=["Місто"]), use_container_width=True, hide_index=True)
        # Виведення таблиці
        with st.expander("Не розприділені дані"):
            st.dataframe(filtered_df[~filtered_df["Територія"].isin(["Територія 1", "Територія 2"])])
        with st.expander("Всі дані по регіону"):
            st.dataframe(filtered_df)
    else:
        region_list = st.selectbox('оберіть регіон',df['Регіон'].unique())
        
        with st.expander("Всі дані по регіону"):
            st.dataframe(filtered_df)
