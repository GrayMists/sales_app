import streamlit as st

def render_sidebar_filters():
    """Відображає фільтри у контейнері"""
    if "df" not in st.session_state:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return
    df = st.session_state.df

    with st.container(border=True):
        st.write("Фільтри")
        st.session_state["selected_region"] = st.selectbox(
            'Оберіть регіон',
            df["Регіон"].unique()
        )

def get_selected_region():
    #Повертає вибраний регіон
    return st.session_state.get("selected_region", None)

def render_sidebar_filters_total_data():
    """Відображає фільтри у контейнері"""
    if "mr_df" not in st.session_state:
        st.warning("Спочатку завантажте файл")
        return
    mr_df = st.session_state.mr_df

    with st.container(border=True):
        st.write("Фільтри")
        st.session_state["selected_region_med_rep"] = st.selectbox(
            'Оберіть населений пункт',
            mr_df["Місто"].unique()
        )

def selected_region_med_rep():
    #Повертає вибраний регіон
    return st.session_state.get("selected_region_med_rep", None)