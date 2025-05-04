from src.api.schemas import CsvDataDTO
from src.config import DB_HOST_, PORT_
from src.repositories.chat_repository import ChatRepository
import httpx


class ChatService:
    def __init__(self, repository: ChatRepository):
        self.repository = repository

    async def get_chat_and_send_api(
            self,
            results: CsvDataDTO
    ):
        try:
            chat_id = await self.repository.get_chat_id()
        except Exception as e:
            print(f"Ошибка подключения к Redis: {e}")
            chat_id = None
        if chat_id:
            dto_dict = results.model_dump()
            result_dto = dto_dict['results']
            timeout = httpx.Timeout(10.0, read=20.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(f"http://{DB_HOST_}:{PORT_}/send_results",
                                             json={"chat_id": chat_id, "results": result_dto})
                if response.status_code == 200:
                    return "Данные отправлены в телеграмм"
                else:
                    print(f"Ошибка при отправке данных в API: статус {response.status_code}, ответ: {response.text}")
                    return "Ошибка при отправке данных в API"
