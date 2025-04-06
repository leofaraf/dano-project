from scipy.stats import norm, stats
import pandas as pd
import numpy as np
import re

def load_earnings():
    return pd.read_csv("NEW_Как_зарабатывают_бобров_КРОК.csv", sep=";")

def load_buyed():
    return pd.read_csv("Покупки_сотрудников_в_боброшопе.csv", sep=";")

def load_staff():
    return pd.read_excel("Список_сотрудников_КРОК.xlsx")


def cases():
    purchases = pd.read_csv("Покупки_сотрудников_в_боброшопе.csv", sep=";")
    earnings = pd.read_csv("NEW_Как_зарабатывают_бобров_КРОК.csv", sep=";")

    purchases["Дата оформления заказа"] = pd.to_datetime(purchases["Дата оформления заказа"], dayfirst=True, errors="coerce")
    earnings["Дата"] = pd.to_datetime(earnings["Дата"], dayfirst=True, errors="coerce")

    categories = purchases["Категория"].unique()

    results_summary = []

    for category in categories:
        cat_purchases = purchases[purchases["Категория"] == category]
        unique_codes = cat_purchases["Код сотрудника"].dropna().unique()[:5]
        
        diff_list = []
        group_before = []
        group_after = []

        for code in unique_codes:
            user_purchases = cat_purchases[cat_purchases["Код сотрудника"] == code]
            if user_purchases.empty:
                continue

            first_purchase_date = user_purchases["Дата оформления заказа"].min()
            user_earnings = earnings[earnings["Код сотрудника"] == code]

            if user_earnings.empty:
                continue

            before = user_earnings[
                (user_earnings["Дата"] < first_purchase_date) &
                (user_earnings["Дата"] >= first_purchase_date - pd.DateOffset(months=3))
            ]

            after = user_earnings[
                (user_earnings["Дата"] > first_purchase_date) &
                (user_earnings["Дата"] <= first_purchase_date + pd.DateOffset(months=3))
            ]

            before_sum = before["Сумма вознаграждения"].sum()
            after_sum = after["Сумма вознаграждения"].sum()
            before_mean = before["Сумма вознаграждения"].mean()
            after_mean = after["Сумма вознаграждения"].mean()

            if pd.isna(before_mean) or pd.isna(after_mean):
                continue

            print("------------------------")
            print("Код сотрудника:", code)
            print("Купил:", category)
            print("Дата:", first_purchase_date)
            print("Доход за 3 месяца до: ", before_sum)
            print("Доход за 3 месяца после: ", after_sum)
            print("------------------------")

        if len(diff_list) < 2:
            continue  # мало данных для анализа

if __name__ == "__main__":
    cases()