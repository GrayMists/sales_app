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