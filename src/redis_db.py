from redis.asyncio import Redis
from src.config import REDIS_HOST, REDIS_PORT


redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
