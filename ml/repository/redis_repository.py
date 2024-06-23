from dataclasses import dataclass

import redis
import redis.asyncio as aredis
from langchain_community.storage import RedisStore

from shared.settings import app_settings


@dataclass
class RedisRepository:
    def __post_init__(self) -> None:
        self.ar = aredis.Redis(
            host=app_settings.redis_host, port=app_settings.redis_port
        )
        self.r = redis.Redis(host=app_settings.redis_host, port=app_settings.redis_port)
        self.rs = RedisStore(client=self.r)

    async def health(self) -> None:
        if not await self.ar.ping():
            raise Exception('non true ping')
