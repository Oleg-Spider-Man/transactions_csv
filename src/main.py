import asyncio
import traceback
# import httpx
from src.redis_db import r
from src.repositories.chat_repository import ChatRepository
from src.repositories.сsv_repository import CsvFileRepository
from src.services.chat_service import ChatService
from src.services.csv_service import CsvService
# from src.utils.analyzer import load_and_process
# from src.utils import analyzer
from src.parse import parse_args
# from src.config import DB_HOST_, PORT_
# from src.redis_db import get_chat_id


async def main():#csv_service: Annotated[CsvService, Depends(play_csv_service)],
               #chat_service: Annotated[ChatService, Depends(play_chat_service)]):
    """Основная функция программы"""
    try:
        args = parse_args()
        dto_results = await CsvService(CsvFileRepository()).load_and_process(args.file, args.start_date, args.end_date)
        await ChatService(ChatRepository(r)).get_chat_and_send_api(dto_results)
        # вызов первого сервиса csv с зависимостью от репо csv

        # dto_results = await csv_service.load_and_process(args.file, args.start_date, args.end_date)
        # await chat_service.get_chat_and_send_api(dto_results)

    # try:
    #     process = await load_and_process(args.file, args.start_date, args.end_date)
    #     results = analyzer.print_results(process)
    #     try:


        # второй сервис со своим репозиторием чата редис пошел


        #     chat_id = await get_chat_id()
        # except Exception as e:
        #     print(f"Ошибка подключения к Redis: {e}")
        #     chat_id = None
        # if chat_id:
        #     timeout = httpx.Timeout(10.0, read=20.0)
        #     async with httpx.AsyncClient(timeout=timeout) as client:
        #         response = await client.post(f"http://{DB_HOST_}:{PORT_}/send_results",
        #                                      json={"chat_id": chat_id, "results": results})
        #         if response.status_code == 200:
        #             return "Данные отправлены в телеграмм"
        #         else:
        #             print(f"Ошибка при отправке данных в API: статус {response.status_code}, ответ: {response.text}")
        #             return "Ошибка при отправке данных в API"
    except Exception as e:
        print(f"Ошибка: {repr(e)}")
        traceback.print_exc()
        return "Ошибка при обработке данных"


if __name__ == "__main__":
    asyncio.run(main())
