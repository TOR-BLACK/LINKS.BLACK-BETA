import pandas as pd


def split_dataframe_generator(df: pd.DataFrame, chunk_size: int = 2500):
    # Используем цикл для разбиения DataFrame на части
    for start in range(0, len(df), chunk_size):
        # Выбираем часть DataFrame с помощью iloc и возвращаем её через yield
        yield df.iloc[start:start + chunk_size]
