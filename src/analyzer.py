import os
import pandas as pd
from typing import Dict, Optional

# Убрал класс


def load_data(file_path: str) -> pd.DataFrame:
    # Загрузка из CSV файла
    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        df = pd.read_csv(file_path)
        required_columns = {'date', 'category', 'amount', 'description'}
        if not required_columns.issubset(df.columns):
            raise ValueError("В файле несоответствие колонок")
        return df
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла: {str(e)}")


def filter_by_dates(
        df: pd.DataFrame,
        start_date: Optional[str],
        end_date: Optional[str]
        ) -> pd.DataFrame:
    # Фильтрация транзакций по датам

    if start_date:
        df = df[df['date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['date'] <= pd.to_datetime(end_date)]
        # Проверяем, что даты корректны
    if df['date'].isnull().any():
        raise ValueError("В файле есть некорректные даты")
    return df


def calculate_by_categories(df: pd.DataFrame) -> Dict[str, float]:
    grouped = df.groupby('category')['amount'].sum()
    return grouped.to_dict()


def print_results(results: Dict[str, float]) -> Dict[str, float]:
    # Вывод результатов в консоль
    total = sum(results.values())
    for category, amount in results.items():
        print(f"{category}: {amount:.2f}")
    print(f"Итого: {total:.2f}")
    results_with_total = results.copy()
    results_with_total["Итого"] = total
    return results_with_total


def format_results_for_bot(results: Dict[str, float]) -> str:
    lines = []
    for category, amount in results.items():
        lines.append(f"{category}: {amount:.2f}")
    return "\n".join(lines)
