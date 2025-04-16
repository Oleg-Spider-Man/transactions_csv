import httpx
import uvicorn
from fastapi import HTTPException, FastAPI
from src.analyzer import format_results_for_bot
from src.api.schemas import ChatidAndResults
from src.config import TELEGRAM_API_URL

app = FastAPI()


@app.post("/send_results", response_model=dict)
async def send_results(chat_id_and_results: ChatidAndResults):  # chat_id: int = Body(None, example=123456789)
    # если больше одного параметра, свагер объединяет
    # автоматически в словарь и меняет пример на тот что был.
    # чат айди и словарь. 2. описание для метода скорее всего описание в свагер
    try:
        text = format_results_for_bot(chat_id_and_results.results)

        async with httpx.AsyncClient() as client:  # не стал client в зависимость ставить
            response = await client.post(
                TELEGRAM_API_URL,
                json={"chat_id": chat_id_and_results.chat_id, "text": text}
            )

        if response.status_code != 200 or not response.json().get("ok", False):
            raise HTTPException(status_code=500, detail="Не удалось отправить сообщение в Telegram")

        return {"status": "success", "chat_id": chat_id_and_results.chat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
