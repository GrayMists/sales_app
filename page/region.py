import streamlit as st
from sidebar_filter.sidebar import get_selected_region


def show_data():
    # Перевірка, чи є дані
    if "df" not in st.session_state:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return
    df = st.session_state.df

    def show_region_columns(df):
        # Отримуємо унікальні регіони
        unique_regions = df["Регіон"].unique()
        
        # Створюємо стільки колонок, скільки унікальних регіонів
        cols = st.columns(len(unique_regions))
        
        # Проходимо по кожному регіону і відображаємо дані в колонці
        for idx, region in enumerate(unique_regions):
            with cols[idx]:
                with st.container(border=True):
                    st.subheader(f"Область: {region}", divider=True)
                    # Тут можна додати будь-яку загальну інформацію для цього регіону
                    region_data = df[df["Регіон"] == region]
                    st.write(f"К-сть упаковок: {region_data['Кількість'].sum() if 'Кількість' in df.columns else 'Немає даних'}")
                    with st.expander("ТОП-5",icon="⬇️"):
                        st.write(region_data.groupby('Найменування')['Кількість'].sum().sort_values(ascending=False).head(5))
                    with st.expander("Продажі",icon="⬇️"):
                        st.write(region_data.groupby('Найменування')['Кількість'].sum())

    show_region_columns(df)
    district_filter = get_selected_region()

    st.write(df[df["Регіон"] == district_filter])