from dictionaries.dictionary_to_clear import remove_values_from_ternopil

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

#Функцію очищення колонки адреси, та отримання нових колонок міста, вулиці та номеру бодинку
#region_name,city_values, street_value, territory_mr, street_mr, products_dict
def clean_delivery_address(df, column,  region_values):
    df[column] = (
        df[column]
        .apply(lambda x: remove_unwanted(x, region_values=region_values))
    )
    return df

def process_filtered_df(df, region_name):

    # Логіка для того щоб датасет очищався з допомогою відповідних словників під регіон
    if region_name == "Тернопільська":
        region_values = remove_values_from_ternopil
        city_values = {}
        street_value = {}
        street_mr = {}
    elif region_name == "Івано-Франківська":
        region_values = {}
        city_values = {}
        street_value = {}
        street_mr = {}   

    col = "Факт.адресадоставки"

    df = clean_delivery_address(df, col, region_values)

    return df

#, region_values, city_values, street_value, territory_mr, street_mr, products_dict