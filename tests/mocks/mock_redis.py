from unittest.mock import AsyncMock


class MockRedis:
    def __init__(self):
        self.set = AsyncMock()
        self.get = AsyncMock(return_value="12345")
