import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from src.config import BOT_TOKEN
from src.redis_db import redis_factory
from src.repositories.chat_repository import ChatRepository
from src.services.bot_service import BotService

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        chat_id = message.chat.id
        redis_client = await redis_factory.create_client()
        repo = ChatRepository(redis_client)
        await BotService(repo).save_chat_id(chat_id)
        await message.answer("Ваш chat_id сохранён!")
    except Exception as e:
        logging.exception(f"Ошибка при обработке /start: {e}")


if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling(bot))
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")
