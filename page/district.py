import streamlit as st


def show_data():
    if "user" in st.session_state:
        user = st.session_state["user"]
        email = user.email
    # Перевірка, чи є дані
    if "df" not in st.session_state:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return
    df = st.session_state.df
    #Перевірка на користувача. 
    #Щоб Інформація фільтрувалась під користувача і в подальшому оброблялась
    if email == "andrew.puliak@gmail.com":
        df_for_mr = df[df["Регіон"] == "24. Тернопіль"]
                
    st.write(df_for_mr)
