import redis.asyncio as redis
from src.config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)


async def save_chat_id(chat_id: int):
    await r.set("chat_id", chat_id)


async def get_chat_id():
    chat_id = await r.get("chat_id")
    if chat_id is not None:
        return int(chat_id)
    return None
