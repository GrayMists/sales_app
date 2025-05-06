import streamlit as st
import pandas as pd
from data_cleaner import process_filtered_df
from user_utils import get_users_profile




def show_data():

    # Перевірка наявності даних у сесії
    profile = st.session_state.get("profile")
    if not profile:
        st.warning("Не знайдено профіль користувача.")
        return

    region = profile.get("region")
    line = profile.get("line")
    user_type = profile.get("type")
    city_raw = profile.get("city")
    if isinstance(city_raw, str):
        city = [c.strip() for c in city_raw.split(",")]
    else:
        city = city_raw
    full_name = profile.get("full_name")

    # Перевірка, чи є дані
    df = st.session_state.get("df")
    if df is None:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return
    #Логіка якщо зайшов користувач з типом адмін, в нього має бути доступ до всіх регіонів
    if user_type == "admin":
        select_region = st.selectbox(
            "Оберіть регіон",
            df["Регіон"].unique(),
            index=df["Регіон"].unique().tolist().index(region) if region in df["Регіон"].unique() else 0
        )

        # Логіка для присвоєння міста в залежності від вибраного регіону
        if region == "Тернопільська":
            selected_city = "м.Тернопіль"
        elif region == "Івано-Франківська":
            selected_city = "м.Івано-Франківськ"
        elif region == "Ужгородська":
            selected_city = "м.Ужгород"
        else:
            selected_city = city  # Якщо місто не вказано, використовуємо значення за замовчуванням
    
        filtered_df = process_filtered_df(df, select_region, selected_city)
    else:
        filtered_df = process_filtered_df(df, region, city[0])
    #Якщо зайшов користувач з типом не адмін
    if user_type != "admin":
        # Фільтрація та обробка даних
        if profile["line"] == "Загальна":
            mr_df = filtered_df[
                (filtered_df["Територія"] == profile["territory"]) &
                (filtered_df["Лінія"].isin(["Лінія 1", "Лінія 2"]))
            ]
        else:
            mr_df = filtered_df[
                (filtered_df["Територія"] == profile["territory"]) &
                (filtered_df["Лінія"] == profile["line"])
            ]
        # зберігаємо інформацію
        st.session_state["mr_df"] = mr_df
        st.subheader(f"Дані по території користувача {full_name}")


        # Групування по продуктах з загальною сумою продаж
        group_by_product = mr_df.groupby("Найменування")["Кількість"].sum().reset_index()
        # Групування по населених пунктах з сумою продаж
        group_by_city = mr_df.groupby("Місто")["Кількість"].sum().reset_index()

        #будуємо колонки для відображення інформації
        col1, col2 = st.columns([2,5])

        with col1:
            st.markdown("""
              ##### Загальні продажі
            """)
            # відображення в 1 колонці загальні продажі по продуктах
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
                
            with st.expander("Продажі у вибраному населеному пункті (натисніть для перегляду)",icon="⬇️"):
                col5, col6 = st.columns([2,3])
                with col5:
                    unique_city = st.selectbox(
                        'Оберіть населений пункт',
                        mr_df["Місто"].unique(),
                        key='select_city'
                    )
                    filtered_streets = mr_df[mr_df["Місто"] == unique_city]["Вулиця"].unique()
                    unique_street = st.selectbox(
                        'Оберіть вулицю',
                        filtered_streets,
                        key='select_streer'
                    )
                with col6:
                    group_by_city_product = mr_df[mr_df["Місто"] == unique_city].groupby(["Місто", "Найменування"])["Кількість"].sum().reset_index()
                    st.text('Продажі в обраному населеному пункті')
                    st.dataframe(group_by_city_product, use_container_width=True, hide_index=True)
            
                temp_df = mr_df[(mr_df["Місто"] == unique_city) & (mr_df["Вулиця"] == unique_street)].copy()
                temp_df["Адреса"] = temp_df["Вулиця"] + ", " + temp_df["Номер будинку"]
                group_by_street_product = temp_df.groupby(["Місто", "Адреса", "Найменування"])["Кількість"].sum().reset_index()
                st.dataframe(group_by_street_product.drop(columns=["Місто"]), use_container_width=True, hide_index=True)
                st.write(group_by_street_product.pivot_table(index=['Адреса'], columns=["Найменування"], values=["Кількість"], fill_value=0))
        # Виведення таблиці
        with st.expander("Не розприділені дані"):
            st.dataframe(filtered_df[~filtered_df["Територія"].isin(["Територія 1", "Територія 2"])])
        with st.expander("Всі дані по регіону"):
            st.dataframe(filtered_df)
    else:
        
        users = get_users_profile()

        # Перевірка на порожні дані
        if users.empty:
            st.warning("Не знайдено даних про користувачів.")
        else:
            med_rep = users[(users['region'] == select_region) & (users['type'] != 'admin')]
            
            if med_rep.empty:
                st.warning("Не знайдено медпредставників для вибраного регіону.")
            else:
                med_rep = med_rep.drop(['id', 'email', "nickname"], axis=1).reset_index(drop=True)

                tab_titles = [f"{user}" for user in med_rep["full_name"]]
                tabs = st.tabs(tab_titles)

                for tab, (_, user_row) in zip(tabs, med_rep.iterrows()):
                    with tab:
                        st.subheader(f"Дані для {user_row['full_name']}")
                        if user_row["line"] == "Загальна":
                            mr_df = filtered_df[
                                (filtered_df["Територія"] == profile["territory"]) &
                                (filtered_df["Лінія"].isin(["Лінія 1", "Лінія 2"]))
                            ]
                        else:
                            mr_df = filtered_df[
                                (filtered_df["Територія"] == profile["territory"]) &
                                (filtered_df["Лінія"] == user_row["line"])
                            ]


                        if med_rep_final_df.empty:
                            st.write(med_rep)
                            st.info("Немає даних для цього медпредставника.")
                            st.write(filtered_df)
                        else:
                            with st.expander("Таблиця продаж"):
                                st.dataframe(med_rep_final_df, use_container_width=True)
                            # Групування по продуктах з загальною сумою продаж
                            group_by_product_med_rep = med_rep_final_df.groupby("Найменування")["Кількість"].sum().reset_index()
                            # Групування по населених пунктах з сумою продаж
                            group_by_city_med_rep = med_rep_final_df.groupby("Місто")["Кількість"].sum().reset_index()
                            col1, col2 = st.columns([2,5])

                            with col1:
                                st.markdown("""
                                ##### Загальні продажі
                                """)
                                # відображення в 1 колонці загальні продажі по продуктах
                                st.dataframe(group_by_product_med_rep, use_container_width=True, hide_index=True, height=(len(group_by_product_med_rep) * 36))
                            with col2:
                                col3, col4 = st.columns(2)
                                
                                with col3:
                                    st.markdown("""
                                    ##### ТОП-5 найкращих
                                    """)
                                    st.dataframe(group_by_product_med_rep.sort_values(by = "Кількість", ascending=False).head(5),  hide_index=True)

                                    st.markdown("""
                                    ##### ТОП-5 найгірших
                                    """)
                                    st.dataframe(group_by_product_med_rep.sort_values(by = "Кількість", ascending=True).head(5),  hide_index=True)

                                        
                                with col4:
                                    st.markdown("""##### Продажі в населених пунктах""")
                                    st.dataframe(group_by_city_med_rep, use_container_width=True, hide_index=True, height=487)
                                
                                with st.expander("Продажі у вибраному населеному пункті (натисніть для перегляду)",icon="⬇️"):
                                    col7, col8 = st.columns([2,3])
                                    with col7:
                                        unique_city = st.selectbox(
                                            'Оберіть населений пункт',
                                            med_rep_final_df["Місто"].unique(),
                                            key=f'select_city_med_rep_{user_row["full_name"]}'
                                        )
                                        filtered_streets = med_rep_final_df[med_rep_final_df["Місто"] == unique_city]["Вулиця"].unique()
                                        unique_street = st.selectbox(
                                            'Оберіть вулицю',
                                            filtered_streets,
                                            key=f'select_streer_med_rep_{user_row["full_name"]}'
                                        )

                                    with col8:
                                        group_by_city_product = med_rep_final_df[med_rep_final_df["Місто"] == unique_city].groupby(["Місто", "Найменування"])["Кількість"].sum().reset_index()
                                        st.text('Продажі в обраному населеному пункті')
                                        st.dataframe(group_by_city_product, use_container_width=True, hide_index=True)
                                    #group_by_street_product = med_rep_final_df[(med_rep_final_df["Місто"] == unique_city) & (med_rep_final_df["Вулиця"] == unique_street)].groupby(["Місто","Вулиця","Номер будинку", "Найменування"])["Кількість"].sum().reset_index()
                                    temp_df = med_rep_final_df[(med_rep_final_df["Місто"] == unique_city) & (med_rep_final_df["Вулиця"] == unique_street)].copy()
                                    temp_df["Адреса"] = temp_df["Вулиця"] + ", " + temp_df["Номер будинку"]
                                    group_by_street_product = temp_df.groupby(["Місто", "Адреса", "Найменування"])["Кількість"].sum().reset_index()
                                    st.dataframe(group_by_street_product.drop(columns=["Місто"]), use_container_width=True, hide_index=True)
                                    st.write(group_by_street_product.pivot_table(index=['Адреса'], columns=["Найменування"], values=["Кількість"], fill_value=0))
                      

