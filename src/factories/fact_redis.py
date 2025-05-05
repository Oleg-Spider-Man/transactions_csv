from abc import ABC, abstractmethod
from redis.asyncio import Redis


class AbstractRedisClientFactory(ABC):
    @abstractmethod
    async def create_client(self):
        pass


class RedisClientFactory(AbstractRedisClientFactory):
    def __init__(self, host, port, db=0, decode_responses=True):
        self.host = host
        self.port = port
        self.db = db
        self.decode_responses = decode_responses

    async def create_client(self):
        return Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=self.decode_responses
        )
