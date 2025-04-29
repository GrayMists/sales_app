import streamlit as st
from streamlit_option_menu import option_menu

from data_loader import df_make
from page.district import show_data as district_data
from sidebar_filter.sidebar import render_sidebar_filters as sidebar_data

with st.sidebar:

    selected = option_menu(
        menu_title=None,
        options=["Головна","Завантаження", "Регіони", "Область"],
        icons=["house","cloud-upload","back" ,"bar-chart"],
        menu_icon="cast",
        default_index=0,
        #orientation="horizontal",
        key="main_menu" 
    )
    if selected == "Завантаження":
        df_make()
    elif selected == "Область":
        sidebar_data()


if selected == "Головна":
    st.warning("Спочатку завантажте файл на сторінці \"Завантаження\" в бічній панелі")
elif selected == "Завантаження":
    if "df" not in st.session_state:
        st.warning("Спочатку завантажте файл на сторінці в бічній панелі")
    else:
        st.success("Дані успішно завантажено, оберіть відповідну сторінку в бічній панелі для подальшої роботи")
        st.write(st.session_state.df)
elif selected == "Область":
    st.write("Тут буде відображатись інформація щодо продаж в обраній області")
    district_data()
elif selected == "Регіони":
    st.write("Тут буде відображатись інформація для порівння регіонів")
#st.write(df)