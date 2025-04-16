from typing import Dict
import httpx
import uvicorn
from fastapi import HTTPException, FastAPI
from src.api.schemas import ResultsPayload
from src.config import BOT_TOKEN


app = FastAPI()


def format_results(results: Dict[str, float]) -> str:
    lines = []
    for category, amount in results.items():
        lines.append(f"{category}: {amount:.2f}")
    return "\n".join(lines)


TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@app.post("/send_results", response_model=dict)
async def send_results(payload: ResultsPayload ):# чат айди и словарь
    text = format_results(payload.results)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            TELEGRAM_API_URL,
            json={"chat_id": payload.chat_id, "text": text}
        )

    if response.status_code != 200 or not response.json().get("ok", False):
        raise HTTPException(status_code=500, detail="Не удалось отправить сообщение в Telegram")

    return {"status": "success", "chat_id": payload.chat_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
