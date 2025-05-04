from src.repositories.chat_repository import ChatRepository


class BotService:
    def __init__(self, repository: ChatRepository):
        self.repository = repository
    # Сервис нужен для логирования. Без него можно и просто репо было

    async def save_chat_id(self, chat_id: int) -> bool:
        return await self.repository.save_chat_id(chat_id)
