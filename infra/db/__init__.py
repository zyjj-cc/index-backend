from surrealdb import AsyncSurreal

from infra.config import Config


class Db:
    def __init__(self, config: Config):
        self.__client = AsyncSurreal(config.db_url)
        self.__config = config

    async def init(self):
        await self.__client.signin({"username": self.__config.db_username, "password": self.__config.db_password})
        await self.__client.use(self.__config.db_namespace, self.__config.db_name)

    async def select(self, table: str):
        return await self.__client.select(table)
