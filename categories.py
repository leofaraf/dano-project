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

def categories():
    df = load_buyed()
    grouped = df.groupby('Категория').size().reset_index(name='Количество записей')
    sorted_grouped = grouped.sort_values(by='Количество записей', ascending=False)
    print(sorted_grouped)

if __name__ == "__main__":
    categories()