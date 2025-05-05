from abc import ABC, abstractmethod
from src.repositories.chat_repository import ChatRepository


class AbstractBotService(ABC):
    @abstractmethod
    async def save_chat_id(self, chat_id: int) -> bool:
        pass


class BotService(AbstractBotService):
    def __init__(self, repository: ChatRepository):
        self.repository = repository
    # Сервис нужен для логирования. Без него можно и просто репо было

    async def save_chat_id(self, chat_id: int) -> bool:
        return await self.repository.save_chat_id(chat_id)
