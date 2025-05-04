import httpx
from fastapi import HTTPException
from src.api.schemas import ChatidAndResults
from src.config import TELEGRAM_API_URL
from src.utils.analyzer import format_results_for_bot


class ApiService:
    @staticmethod  # когда добавлю логирование ститик убрать
    async def send_results(chat_id_and_results: ChatidAndResults):
        try:
            text = format_results_for_bot(chat_id_and_results.results)

            async with httpx.AsyncClient() as client:
                response = await client.post(TELEGRAM_API_URL,
                                             json={"chat_id": chat_id_and_results.chat_id, "text": text}
                                             )
                if response.status_code != 200 or not response.json().get("ok", False):
                    raise HTTPException(status_code=500, detail="Не удалось отправить сообщение в Telegram")

            return {"status": "success", "chat_id": chat_id_and_results.chat_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
