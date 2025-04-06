import pandas as pd
import numpy as np
import re

def load_earnings():
    return pd.read_csv("NEW_Как_зарабатывают_бобров_КРОК.csv", sep=";")

def load_buyed():
    return pd.read_csv("Покупки_сотрудников_в_боброшопе.csv", sep=";")

def load_staff():
    return pd.read_excel("Список_сотрудников_КРОК.xlsx")

def load_rfm():
    return pd.read_excel("staff_rfm.xlsx")

# Функция для преобразования стажа в число месяцев
def convert_to_months(staj_str):
    # Регулярные выражения для поиска чисел в строках
    years_match = re.search(r'(\d+)\s*г', staj_str)
    months_match = re.search(r'(\d+)\s*м', staj_str)
    
    # Инициализируем годы и месяцы по умолчанию
    years = 0
    months = 0
    
    # Если нашли годы, то присваиваем их
    if years_match:
        years = int(years_match.group(1))
    
    # Если нашли месяцы, то присваиваем их
    if months_match:
        months = int(months_match.group(1))
    
    # Преобразуем всё в месяцы
    total_months = years * 12 + months
    return total_months

# Функция для группировки по стажу
def staj_group(staj_months):
    if staj_months <= 6:
        return 'до полугода'
    elif staj_months <= 12:
        return 'до года'
    elif staj_months <= 24:
        return 'до 2 лет'
    elif staj_months <= 60:
        return 'до 5 лет'
    else:
        return 'больше 5 лет'

def main():
    # Загружаем данные
    df = load_rfm()

    df['Стаж (месяцы)'] = df['Стаж фактический по компании'].apply(convert_to_months)
    df['Группа по стажу'] = df['Стаж (месяцы)'].apply(staj_group)

    df.to_excel("grouped_by_exp.xlsx")

if __name__ == "__main__":
    main()