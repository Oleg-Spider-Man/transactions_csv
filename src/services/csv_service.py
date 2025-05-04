# здесь логика из main которая берет данные из парсера анализирует их функцией
# и второй функцией создает результат
from collections import defaultdict
from datetime import datetime
from typing import Optional
from src.api.schemas import CsvDataDTO
from src.parse import parse_args
from src.repositories.сsv_repository import CsvFileRepository


class CsvService:
    def __init__(self, repository: CsvFileRepository):
        self.repository = repository

    async def load_and_process(
            self,
            file_path: str,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None
    ) -> CsvDataDTO:

        await self.repository.check_file(file_path)
        # Преобразуем даты фильтрации в объекты datetime.date
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None

        category_sums = defaultdict(float)  # при обращении если ключа нет создаст с заданным значением 0.0

        header_line = await self.repository.check_headers(file_path)
        headers = header_line.strip().split(',')

        required_columns = {'date', 'category', 'amount', 'description'}

        if not required_columns.issubset(set(headers)):
            raise ValueError("В файле несоответствие колонок")

        # Индексы колонок. Если порядок будет не правильный от клиента
        idx_date = headers.index('date')
        idx_category = headers.index('category')
        idx_amount = headers.index('amount')

        async for line in self.repository.get_rows(file_path):
            parts = line.strip().split(',', maxsplit=3)
            if len(parts) < 4:
                continue  # если колонок меньше чем надо, пропускаем строку итерации

            date_str = parts[idx_date]
            category = parts[idx_category]
            amount_str = parts[idx_amount]

            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Некорректная дата в строке: {line.strip()}")

            # Фильтрация по дате
            if start_dt and date_obj < start_dt:
                continue
            if end_dt and date_obj > end_dt:
                continue

            try:
                amount = float(amount_str)
            except ValueError:
                raise ValueError(f"Некорректное число amount в строке: {line.strip()}")

            category_sums[category] += amount

        total = sum(category_sums.values())
        for category, amount in category_sums.items():
            print(f"{category}: {amount:.2f}")
        print(f"Итого: {total:.2f}")
        results_with_total = category_sums.copy()  # что бы не менять исходный словарь
        results_with_total["Итого"] = total
        return CsvDataDTO(results=results_with_total)

