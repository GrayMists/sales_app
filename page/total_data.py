import streamlit as st



def show_data():
    # Перевірка, чи є дані
    if "df" not in st.session_state:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return
    df = st.session_state.df
    district_filter = st.selectbox(
            'Оберіть регіон',
            df["Регіон"].unique()
        )
    st.write(df[df["Регіон"] == district_filter])