import os

import pandas as pd
from typing import Dict, Optional
import redis


class FinanceAnalyzer:
    def __init__(self, file_path: str):
        self.redis_client = redis.Redis(host='localhostааа', port=6379, decode_responses=True)
        self.file_path = file_path

    @staticmethod
    def _get_cache_key(start_date: Optional[str], end_date: Optional[str]) -> str:
        # Если дата не указана, используем специальный маркер
        start = start_date if start_date else "*"
        end = end_date if end_date else "*"
        return f"data_{start}_{end}"

    def load_data(self) -> pd.DataFrame:
        # Загрузка из CSV файла
        try:
            if not os.path.isfile(self.file_path):
                raise FileNotFoundError(f"Файл не найден: {self.file_path}")
            df = pd.read_csv(self.file_path)
            required_columns = {'date', 'category', 'amount', 'description'}
            if not required_columns.issubset(df.columns):
                raise ValueError("В файле несоответствие колонок")
            return df
        except Exception as e:
            raise ValueError(f"Ошибка при чтении файла: {str(e)}")

    @staticmethod
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

    @staticmethod
    def calculate_by_categories(df: pd.DataFrame) -> Dict[str, float]:
        # """Расчет сумм по категориям"""
        # # Сначала получаем уникальное имя для этих данных
        # cache_key = _get_cache_key(start_date, end_date)
        #
        # # Проверяем есть ли эти данные в кеше
        # cached_data = self.redis_client.get(cache_key)
        # if cached_data:
        #     print(f"Данные загружены из кэша для периода {start_date}-{end_date}")
        #     return json.loads(cached_data)

        # Если данных нет в кеше - вычисляем новые
        grouped = df.groupby('category')['amount'].sum()
        return grouped.to_dict()

    @staticmethod
    def print_results(results: Dict[str, float]) -> Dict[str, float]:
        """Вывод результатов в консоль"""
        total = sum(results.values())
        for category, amount in results.items():
            print(f"{category}: {amount:.2f}")
        print(f"\nИтого: {total:.2f}")
        results_with_total = results.copy()
        results_with_total["Итого"] = total
        return results_with_total
