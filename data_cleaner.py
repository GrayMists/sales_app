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
