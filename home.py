import streamlit as st
from streamlit_option_menu import option_menu

from data_loader import df_make
from page.district import show_data as district_data
from page.total_data import show_data as total_data
from page.region import show_data as region_data
from sidebar_filter.sidebar import render_sidebar_filters as sidebar_data
from page.login import show_login_data as login

if "user" not in st.session_state:
    login()
    st.stop()

with st.sidebar:
    if "user" in st.session_state:
        user = st.session_state["user"]
        full_name = user.user_metadata.get("full_name", "Користувач")
        email = user.email
    with st.container(border=True):
        st.markdown(
            f"<h3 style='text-align: center;'>👤 {full_name}</h3>"
            f"<h4 style='text-align: center;'>{email}</h4>",
            unsafe_allow_html=True
        )
    selected = option_menu(
        menu_title=None,
        options=["Головна","Регіони", "Область"],
        icons=["house","back" ,"bar-chart"],
        menu_icon="cast",
        default_index=0,
        #orientation="horizontal",
        key="main_menu" 
    )
    if selected == "Регіони":
        sidebar_data()


if selected == "Головна":
    if "df" not in st.session_state:
        st.warning("Спочатку завантажте файл")
        df_make()
    else:
        st.success("Дані успішно завантажено, оберіть відповідну сторінку в бічній панелі для подальшої роботи")
        total_data()
elif selected == "Область":
    st.write("Тут буде відображатись інформація щодо продаж в області представника що увійшов")
    district_data()
elif selected == "Регіони":
    st.write("Тут буде відображатись інформація для порівння регіонів")
    region_data()
#st.write(df)