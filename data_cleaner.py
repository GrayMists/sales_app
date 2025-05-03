import pandas as pd
from dictionaries.dictionary_to_clear import (
    remove_values_from_ternopil,
    remove_values_from_frankivsk
)
from dictionaries.replacment_city_dictionaries import (
    replace_ternopil_city_dict,
    replace_frankivsk_city_dict
)
from dictionaries.replacement_street_dictionaries import (
    replace_ternopil_street_dict,
    replace_frankivsk_street_dict
)
from dictionaries.mr_dictionary import (
    territory_ternopil_mr,
    street_ternopil_territory
)
from dictionaries.product_dictionaryes import products_dict
# Функція видалення лишніх знаків та пробілів
def clean_text(series):
    return series.astype(str).apply(lambda x: x.replace('\n', '').replace('\t', '').strip())

def change_district_name(region: str):
    region = str(region).strip()
    if region == "10. Івано-Франк":
        return "Івано-Франківська"
    elif region == "24. Тернопіль":
        return "Тернопільська"
    elif region == "21. Ужгород":
        return "Ужгородська"
  
    return region

# Функція для видалення значень
def remove_unwanted(text, region_values):
    if isinstance(text, str):  # Перевіряємо, чи це рядок
        for val in region_values:
            text = text.replace(val, "")  # Поетапна заміна
    return text.strip()  # Видалення зайвих пробілів
def replacement_city(text, city_values):
    if isinstance(text, str):  # Переконуємось, що значення - це рядок
        for key, value in city_values.items():  # Використовуємо city_values, якщо це словник
            text = text.replace(key, value)  # Поетапна заміна
    return text.strip()  # Видаляємо зайві пробіли
def replacement_street(text, street_values):
    if isinstance(text, str):  # Переконуємось, що значення рядок
        for key, value in street_values.items():
            text = text.replace(key, value)  # Замінюємо ключ на значення
        return text.strip()  # Видаляємо зайві пробіли
#Витягуємо назву міста
def extract_city(address):
        # Витягуємо текст до першої коми
        part_before_comma = address.split(',')[0].strip()
        # Повертаємо текст до коми
        return part_before_comma  
#Функція для отримання назв вулиць
def extract_street(address_street):
    parts = address_street.split(',')
    return parts[1].strip() if len(parts) > 1 else ""  # Перевіряємо, чи є хоча б 2 частини
#Функція для отримання номуру будинку
def extract_num_house(address_street):
    parts = address_street.split(',')
    return parts[2].strip() if len(parts) > 2 else ""  # Перевіряємо, чи є хоча б 3 частини

#Функція яка визначає приналежність до певної території відповідно до міста
def mr_district(text, dict):
    if isinstance(text, str):  # Перевіряємо, чи це рядок
        return dict.get(text, "").strip()
    return text
#Функція яка визначає приналежність до певної території відповідно до вулиці в місті
def update_territory_for_city_streets(df, city_name, street_dict, city):
    def update_row(row):
        if row["Регіон"] == city_name and row["Місто"] == city:
            for street_key, territory in street_dict.items():
                if pd.notna(row["Вулиця"]) and street_key in row["Вулиця"]:
                    return territory
        return row["Територія"]
    
    df["Територія"] = df.apply(update_row, axis=1)
    return df  

#Функція яка визначає приналежність до певної лінії перпарату
def assign_line_from_product_name(name):
        if isinstance(name, str):
            for key in products_dict:
                if key in name:
                    return products_dict[key]
        return None


#Функцію очищення колонки адреси, та отримання нових колонок міста, вулиці та номеру бодинку
def clean_delivery_address(df, column,region_name,  region_values, city_values,street_values,street_mr,territory,city):
    df[column] = (
        df[column]
        .apply(lambda x: remove_unwanted(x, region_values=region_values))
        .apply(lambda x: replacement_city(x, city_values=city_values))
        .apply(lambda x: replacement_street(x, street_values=street_values))
        .str.replace(",,", ",", regex=True)
    )
    df["Місто"] = df[column].apply(extract_city).str.strip()
    df["Вулиця"] = df[column].apply(extract_street).str.strip()
    df["Номер будинку"] = df[column].apply(extract_num_house).str.strip()
     # Додаємо категоризацію по території, для подальшого зручнішого групування
    df["Територія"] = df["Місто"].apply(lambda x: mr_district(x, territory))
    df = update_territory_for_city_streets(df, region_name, street_mr, city)
    df["Лінія"] = df["Найменування"].apply(assign_line_from_product_name)
    return df.reset_index(drop=True)

def process_filtered_df(df, region_name,city):
    df = df[df["Регіон"] == region_name]
    # Логіка для того щоб датасет очищався з допомогою відповідних словників під регіон
    if region_name == "Тернопільська":
        region_values = remove_values_from_ternopil
        city_values = replace_ternopil_city_dict
        street_values = replace_ternopil_street_dict
        street_mr = street_ternopil_territory
        territory = territory_ternopil_mr
    elif region_name == "Івано-Франківська":
        region_values = remove_values_from_frankivsk
        city_values = replace_frankivsk_city_dict
        street_values = replace_frankivsk_street_dict
        street_mr = {}  
        territory = {}  
    elif region_name == "Ужгородська":
        region_values = []
        city_values = {}
        street_values = {}
        street_mr = {}  
        territory = {} 

    col = "Факт.адресадоставки"

    df = clean_delivery_address(df, col,region_name, region_values,city_values,street_values,street_mr,territory,city)

    return df.reset_index(drop=True)
