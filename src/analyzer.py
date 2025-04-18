import os
from typing import Dict, Optional
from datetime import datetime
from collections import defaultdict
import aiofiles


async def load_and_process(
    file_path: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, float]:

    # Асинхронно читает CSV файл построчно(что бы сразу большой файл не читать)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # Преобразуем даты фильтрации в объекты datetime.date
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None

    category_sums = defaultdict(float)  # при обращении если ключа нет создаст с заданным значением 0.0

    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
        header_line = await f.readline()
        headers = header_line.strip().split(',')

        required_columns = {'date', 'category', 'amount', 'description'}
        if not required_columns.issubset(set(headers)):
            raise ValueError("В файле несоответствие колонок")

        # Индексы колонок. Если порядок будет не правильный от клиента
        idx_date = headers.index('date')
        idx_category = headers.index('category')
        idx_amount = headers.index('amount')

        # Читаем файл построчно асинхронно
        #  async for line in f:
        while True:
            line = await f.readline()
            if not line:
                break
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
    return dict(category_sums)


def print_results(results: Dict[str, float]) -> Dict[str, float]:
    total = sum(results.values())
    for category, amount in results.items():
        print(f"{category}: {amount:.2f}")
    print(f"Итого: {total:.2f}")
    results_with_total = results.copy()  # что бы не менять исходный словарь
    results_with_total["Итого"] = total
    return results_with_total


def format_results_for_bot(results: Dict[str, float]) -> str:
    lines = []
    for category, amount in results.items():
        lines.append(f"{category}: {amount:.2f}")
    return "\n".join(lines)
