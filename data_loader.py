import streamlit as st
import pandas as pd




# Функція для отримання CSV-посилання
def get_csv_url(sheet_url):
    try:
        if "/d/" not in sheet_url or "/edit" not in sheet_url:
            return None
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    except IndexError:
        return None


# Функція для отримання даних з excel файлу
def load_url_data(sheet_url):
    csv_url = get_csv_url(sheet_url)
    if not csv_url:
        return None
    try:
        df = pd.read_csv(csv_url)
        df.columns = df.columns.str.replace(" ","")  # Видаляємо пробіли з назв колонок
        excluded_columns = ["Adding", "ЄДРПОУ", "Юр.адресаклієнта"]      
        #, '21. Ужгород' <-- до фільтру тернопіль щоб отримувати тільки ті дані що будуть в фільтрі
        df = df.drop(columns=[col for col in excluded_columns if col in df.columns], errors="ignore")
        df = df[df['Регіон'].isin(["24. Тернопіль", "10. Івано-Франк", "21. Ужгород"])]
        return df
    except Exception as e:
        return f"Помилка при завантаженні: {e}"
    
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
    sheet_url = st.text_input("Вставте посилання на Google Таблицю:")
    load_button = st.button("Завантажити") #Кнопка діє тільки для посилання
    st.divider()
    uploaded_file = st.file_uploader("Оберіть файл")
    
    df = pd.DataFrame()  # Ініціалізуємо df, щоб уникнути помилки при st.write(df)

    if uploaded_file is not None:
        if uploaded_file.name.endswith((".xlsx", ".xls")):
            try:
                df = load_excel_data(uploaded_file)
                st.session_state.df = df
            except Exception as e:
                st.error(f"Помилка при зчитуванні файлу: {e}")
        else:
            st.error("Будь ласка, завантажте Excel-файл (.xlsx або .xls)")
    elif sheet_url and load_button:
        df = load_url_data(sheet_url)
        if isinstance(df, str):
            st.error(df)
            df = pd.DataFrame()
        else:
            st.success("Дані успішно завантажені з посилання!")
            st.session_state.df = df

    if not df.empty:
        st.write("Колонки таблиці:", list(df.columns))