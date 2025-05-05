import asyncio
import traceback
from src.redis_db import redis_factory
from src.repositories.chat_repository import ChatRepository
from src.repositories.сsv_repository import CsvFileRepository
from src.services.chat_service import ChatService
from src.services.csv_service import CsvService
from src.parse import parse_args


async def main():
    """Основная функция программы"""
    try:
        args = parse_args()
        dto_results = await CsvService(CsvFileRepository()).load_and_process(args.file, args.start_date, args.end_date)
        redis_client = await redis_factory.create_client()
        await ChatService(ChatRepository(redis_client)).get_chat_and_send_api(dto_results)

    except Exception as e:
        print(f"Ошибка: {repr(e)}")
        traceback.print_exc()
        return "Ошибка при обработке данных"


if __name__ == "__main__":
    asyncio.run(main())
