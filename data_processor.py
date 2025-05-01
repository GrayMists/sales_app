from data_cleaner import change_district_name, clean_text

def process_excel_df(df):
    df.columns = df.columns.str.replace(" ", "").str.strip()
    excluded_columns = ["Adding", "ЄДРПОУ", "Юр.адресаклієнта"]
    df = df.drop(columns=[col for col in excluded_columns if col in df.columns], errors="ignore")
    allowed_regions = ["24. Тернопіль", "10. Івано-Франк", "21. Ужгород"]
    df = df[df["Регіон"].isin(allowed_regions)]
    df["Регіон"] = df["Регіон"].apply(change_district_name)
    if "Факт.адресадоставки" in df.columns:
        df["Факт.адресадоставки"] = clean_text(df["Факт.адресадоставки"])
    return df.reset_index(drop=True)