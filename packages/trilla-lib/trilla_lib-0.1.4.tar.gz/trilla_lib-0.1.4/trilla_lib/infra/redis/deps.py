import aioredis

from trilla_lib.infra.redis.config import RedisConfig

config = RedisConfig()
client = aioredis.from_url(str(config.url), decode_responses=True)

