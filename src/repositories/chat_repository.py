import logging
from redis.asyncio import Redis
from abc import ABC, abstractmethod


class AbstractChatRepository(ABC):
    @abstractmethod
    async def save_chat_id(self, chat_id: int):
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")

    @abstractmethod
    async def get_chat_id(self) -> int | None:
        raise NotImplementedError("Метод должен быть переопределен в дочернем классе")


class ChatRepository(AbstractChatRepository):
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def save_chat_id(self, chat_id: int):
        try:
            await self.redis.set("chat_id", chat_id)
        except Exception as e:
            logging.error(f"Redis error: {e}")

    async def get_chat_id(self) -> int | None:
        try:
            chat_id = await self.redis.get("chat_id")
            return int(chat_id) if chat_id else None
        except Exception as e:
            logging.error(f"Redis error: {e}")
            return None
