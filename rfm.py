import pandas as pd
import numpy as np

def load_earnings():
    return pd.read_csv("NEW_Как_зарабатывают_бобров_КРОК.csv", sep=";")

def load_buyed():
    return pd.read_csv("Покупки_сотрудников_в_боброшопе.csv", sep=";")

def load_staff():
    return pd.read_excel("Список_сотрудников_КРОК.xlsx")

def most_frequent_items():
    df = load_buyed()
    grouped = df.groupby('Категория').size().reset_index(name='Количество записей')
    sorted_grouped = grouped.sort_values(by='Количество записей', ascending=False)
    print(sorted_grouped)

def staff_with_earnings():
    earnings_df = load_earnings()
    staff_df = load_staff()

    # Считаем сумму бобров по каждому сотруднику
    total_earned = earnings_df.groupby("Код сотрудника")["Сумма вознаграждения"].sum().reset_index()
    total_earned = total_earned.rename(columns={"Код сотрудника": "Внешний код", "Сумма вознаграждения": "Итого бобров"})

    # Объединяем с таблицей сотрудников
    merged_df = staff_df.merge(total_earned, on="Внешний код", how="left")

    # Заменяем NaN на 0 — значит, сотрудник ничего не заработал
    merged_df["Итого бобров"] = merged_df["Итого бобров"].fillna(0).astype(int)

    return merged_df

def rfm_analysis():
    # Загружаем данные
    staff_df = staff_with_earnings()  # Из предыдущей функции
    earnings_df = load_earnings()  # Заработок сотрудников
    purchases_df = load_buyed()  # Покупки сотрудников
    
    # Преобразуем дату в тип datetime, если нужно
    earnings_df["Дата"] = pd.to_datetime(earnings_df["Дата"], errors='coerce')
    
    # Считаем Recency (R) — время с последней активности сотрудника
    last_activity = earnings_df.groupby("Код сотрудника")["Дата"].max().reset_index()
    last_activity = last_activity.rename(columns={"Дата": "Последняя активность"})
    
    # Предположим, что дата анализа — это сегодняшняя дата
    today = pd.to_datetime("16.10.2024")
    last_activity["Recency"] = (today - last_activity["Последняя активность"]).dt.days
    
    # Считаем Frequency (F) — количество активностей каждого сотрудника
    frequency = earnings_df.groupby("Код сотрудника").size().reset_index(name="Frequency")
    
    # Считаем Monetary (M) из покупок — сумма стоимости покупок каждым сотрудником
    purchases_df["Стоимость в валюте"] = pd.to_numeric(purchases_df["Стоимость в валюте"], errors='coerce')
    monetary = purchases_df.groupby("Код сотрудника")["Стоимость в валюте"].sum().reset_index()
    monetary = monetary.rename(columns={"Стоимость в валюте": "Monetary"})
    
    # Объединяем все данные в одну таблицу
    staff_df.columns = staff_df.columns.str.strip()  # Remove any extra spaces from column names
    last_activity.columns = last_activity.columns.str.strip()
    
    # Merge all dataframes correctly
    rfm_df = staff_df.merge(last_activity[["Код сотрудника", "Recency"]], left_on="Внешний код", right_on="Код сотрудника", how="left")
    rfm_df = rfm_df.merge(frequency, left_on="Внешний код", right_on="Код сотрудника", how="left")
    rfm_df = rfm_df.merge(monetary, left_on="Внешний код", right_on="Код сотрудника", how="left")
    
    # Drop the duplicate 'Код сотрудника' columns
    rfm_df = rfm_df.drop(columns=[col for col in rfm_df.columns if 'Код сотрудника' in col])
    
    # Reset the index to remove any residual index
    rfm_df = rfm_df.reset_index(drop=True)
    # rfm_df = rfm_df.drop("Код сотрудника_x", axis=1)
    # rfm_df = rfm_df.drop("Код сотрудника_y", axis=1)
    
    # Заполняем пропуски, если есть
    rfm_df["Recency"] = rfm_df["Recency"].fillna(np.nan)
    rfm_df["Frequency"] = rfm_df["Frequency"].fillna(0)
    rfm_df["Monetary"] = rfm_df["Monetary"].fillna(0)
    
    # Выводим результат
    return rfm_df

def main():
    df = rfm_analysis()
    df.to_excel("staff_rfm.xlsx")
    print(df)

if __name__ == "__main__":
    main()