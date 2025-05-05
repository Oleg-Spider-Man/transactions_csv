# from redis.asyncio import Redis
from src.config import REDIS_HOST, REDIS_PORT
from src.factories.fact_redis import RedisClientFactory

# redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
redis_factory = RedisClientFactory(REDIS_HOST, REDIS_PORT)

