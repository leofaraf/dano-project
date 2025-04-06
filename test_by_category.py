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

def load_rfm():
    return pd.read_excel("staff_rfm.xlsx")

def z_test_by_category():
    purchases = pd.read_csv("Покупки_сотрудников_в_боброшопе.csv", sep=";")
    earnings = pd.read_csv("NEW_Как_зарабатывают_бобров_КРОК.csv", sep=";")

    purchases["Дата оформления заказа"] = pd.to_datetime(purchases["Дата оформления заказа"], dayfirst=True, errors="coerce")
    earnings["Дата"] = pd.to_datetime(earnings["Дата"], dayfirst=True, errors="coerce")

    categories = purchases["Категория"].unique()

    results_summary = []

    print(categories)

    for category in categories:
        cat_purchases = purchases[purchases["Категория"] == category]
        unique_codes = cat_purchases["Код сотрудника"].dropna().unique()
        
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

            group_before.append(before_sum)
            group_after.append(after_sum)
            diff = after_sum - before_sum
            diff_list.append(diff)

        if len(diff_list) < 2:
            continue  # мало данных для анализа

        # z-тест
        diffs = np.array(diff_list)
        sample_mean = np.mean(diffs)

        print(sample_mean)

        sample_std = np.std(diffs, ddof=1)
        n = len(diffs)

        z_score = (sample_mean - 0) / (sample_std / np.sqrt(n))
        p_value =  2*min([1 - norm.cdf(z_score),norm.cdf(z_score)])

        t_stat, p_v = stats.ttest_ind(group_before, group_after)
        print("t-test: ", t_stat, p_v)


        results_summary.append({
            "Категория": category,
            "Кол-во сотрудников": n,
            "Средняя разница": round(sample_mean, 2),
            "Z-статистика": round(z_score, 3),
            "P-значение": round(p_value, 3),
            "Вывод": ("✅ Рост" if sample_mean > 0 else "❌ Отрицательный рост") if p_value < 0.05 else "❌ Нет роста"
        })

    summary_df = pd.DataFrame(results_summary)
    print(summary_df)
    summary_df.to_excel("z_test_by_category.xlsx", index=False)

if __name__ == "__main__":
    z_test_by_category()