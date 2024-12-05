import sys

from redis.asyncio import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from common.logger import logger
from core.config import settings


class RedisCli(Redis):
    def __init__(self):
        super(RedisCli, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True,
        )

    async def open(self):
        try:
            await self.ping()
        except TimeoutError:
            logger.error("Время ожидания повторного подключения к redis вышло")
            sys.exit()
        except AuthenticationError:
            logger.error(
                "Не удалось выполнить проверку подлинности подключения к базе данных redis"
            )
            sys.exit()
        except Exception as e:
            logger.error("Не удалось повторно подключиться к redis {}", e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list = None):
        """
        Удалите все ключи с указанным префиксом

        :param prefix:
        :param exclude:
        :return:
        """
        keys = []
        async for key in self.scan_iter(match=f"{prefix}*"):
            if isinstance(exclude, str):
                if key != exclude:
                    keys.append(key)
            elif isinstance(exclude, list):
                if key not in exclude:
                    keys.append(key)
            else:
                keys.append(key)
        if keys:
            await self.delete(*keys)


redis_client = RedisCli()
