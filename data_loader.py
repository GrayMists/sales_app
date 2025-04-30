import streamlit as st
import pandas as pd



# Функція для отримання даних з excel файлу
def load_excel_data(file):
    df = pd.read_excel(file)
    st.success("Файл успішно завантажено!")
    df.columns = df.columns.str.replace(" ", "")  # Видаляємо пробіли з назв колонок
    excluded_columns = ["Adding", "ЄДРПОУ", "Юр.адресаклієнта"]
    df = df.drop(columns=[col for col in excluded_columns if col in df.columns], errors="ignore")
    df = df[df['Регіон'].isin(["24. Тернопіль", "10. Івано-Франк", "21. Ужгород"])]
    df = df.reset_index(drop=True)
    return df

def df_make():
    st.divider()
    uploaded_file = st.file_uploader("Оберіть файл")
    
    df = pd.DataFrame()  # Ініціалізуємо df, щоб уникнути помилки при st.write(df)

    if uploaded_file is not None:
        if uploaded_file.name.endswith((".xlsx", ".xls")):
            try:
                df = load_excel_data(uploaded_file)
                st.session_state.df = df
                st.rerun()
            except Exception as e:
                st.error(f"Помилка при зчитуванні файлу: {e}")
        else:
            st.error("Будь ласка, завантажте Excel-файл (.xlsx або .xls)")

    