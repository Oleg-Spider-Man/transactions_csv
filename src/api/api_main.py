import uvicorn
from fastapi import FastAPI
from src.services.api_service import ApiService
from src.api.schemas import ChatidAndResults, Response


app = FastAPI()


@app.post("/send_results", response_model=Response)
async def send_results(chat_id_and_results: ChatidAndResults):  # chat_id: int = Body(None, example=123456789)
    await ApiService().send_results(chat_id_and_results)
    return {"status": "success", "chat_id": chat_id_and_results.chat_id}


    # Если больше одного параметра, свагер объединяет
    # автоматически в словарь и меняет заданный пример на стандартный тот что был.
    # Я изменил пример в сваггер с помощью класса config в схеме. Теперь в документации есть пример
    # ключей и значений словаря.


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
