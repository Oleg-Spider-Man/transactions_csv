import asyncio
import httpx
from src.analyzer import FinanceAnalyzer, pd
from src.parse import parse_args
from src.config import DB_HOST_, PORT_
from src.redis_db import get_chat_id


async def main():
    """Основная функция программы"""
    args = parse_args()

    analyzer = FinanceAnalyzer(args.file)

    try:
        # Загрузка и фильтрация данных
        df = analyzer.load_data()
        df['date'] = pd.to_datetime(df['date'])

        df = analyzer.filter_by_dates(df, args.start_date, args.end_date)

        # Расчет результатов
        results = analyzer.calculate_by_categories(df)

        # Вывод результатов в консоль
        analyzer.print_results(results)
        results = analyzer.print_results(results)

        # отправка в телегу если есть чат
        try:
            chat_id = await get_chat_id()
            print(f"Полученный chat_id: {chat_id!r}")
        except Exception as e:
            print(f"Ошибка подключения к Redis: {e}")
            chat_id = None
        if chat_id:
            # httpx отправка на эндпоинт а с него в телегу
            async with httpx.AsyncClient() as client:
                response = await client.post(f"http://{DB_HOST_}:{PORT_}/send_results", json={"chat_id": chat_id,
                                                                                              "results": results})
                if response.status_code == 200:
                    return "Данные отправленны в телеграмм"

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return "Ошибка при обработке данных"


if __name__ == "__main__":
    asyncio.run(main())
