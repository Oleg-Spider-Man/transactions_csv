import logging
import redis.asyncio as redis
from src.config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)


async def save_chat_id(chat_id: int):
    try:
        await r.set("chat_id", chat_id)
    except redis.RedisError as e:
        logging.error(f"Ошибка при сохранении chat_id: {e}")


async def get_chat_id():
    try:
        chat_id = await r.get("chat_id")
        if chat_id is not None:
            return int(chat_id)
        return None
    except redis.RedisError as e:
        logging.error(f"Ошибка при получении chat_id: {e}")
        return None
