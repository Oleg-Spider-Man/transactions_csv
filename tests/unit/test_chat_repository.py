import pytest

from src.repositories.chat_repository import ChatRepository
from tests.mocks.mock_redis import MockRedis


@pytest.mark.asyncio
async def test_save_and_get_chat_id():
    mock_redis = MockRedis()
    repo = ChatRepository(mock_redis)  # type: ignore

    # Тестируем сохранение
    await repo.save_chat_id(12345)
    mock_redis.set.assert_awaited_once_with("chat_id", 12345)

    # Тестируем получение
    chat_id = await repo.get_chat_id()
    assert chat_id == 12345
    mock_redis.get.assert_awaited_once_with("chat_id")
