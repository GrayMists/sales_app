import streamlit as st
import pandas as pd
from data_processor import process_excel_df


def load_excel_data(file):
    return pd.read_excel(file)

def df_make():
    st.divider()
    uploaded_file = st.file_uploader("Оберіть файл")
    
    df = pd.DataFrame()  # Ініціалізуємо df, щоб уникнути помилки при st.write(df)

    if uploaded_file is not None:
        if uploaded_file.name.endswith((".xlsx", ".xls")):
            try:
                df = load_excel_data(uploaded_file)
                df = process_excel_df(df)
                st.session_state.df = df
                st.rerun()
            except Exception as e:
                st.error(f"Помилка при зчитуванні файлу: {e}")
        else:
            st.error("Будь ласка, завантажте Excel-файл (.xlsx або .xls)")