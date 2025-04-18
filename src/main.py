import asyncio
import httpx
from src.analyzer import load_and_process
from src import analyzer
from src.parse import parse_args
from src.config import DB_HOST_, PORT_
from src.redis_db import get_chat_id


async def main():
    """Основная функция программы"""
    args = parse_args()

    try:
        process = await load_and_process(args.file, args.start_date, args.end_date)
        results = analyzer.print_results(process)
        try:
            chat_id = await get_chat_id()
        except Exception as e:
            print(f"Ошибка подключения к Redis: {e}")
            chat_id = None
        if chat_id:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"http://{DB_HOST_}:{PORT_}/send_results", json={"chat_id": chat_id,
                                                                                              "results": results})
                if response.status_code == 200:
                    return "Данные отправлены в телеграмм"

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return "Ошибка при обработке данных"


if __name__ == "__main__":
    asyncio.run(main())
