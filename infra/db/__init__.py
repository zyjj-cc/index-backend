from surrealdb import AsyncSurreal, RecordID

from infra.config import Config


class Db:
    def __init__(self, config: Config):
        self.__client = AsyncSurreal(config.db_url)
        self.__config = config

    async def start(self):
        await self.__client.signin({"username": self.__config.db_username, "password": self.__config.db_password})
        await self.__client.use(self.__config.db_namespace, self.__config.db_name)

    async def stop(self):
        await self.__client.close()

    async def select_all(self, table: str):
        return await self.__client.select(table)

    async def select_id(self, table: str, record_id: str):
        return await self.__client.select(RecordID(table, record_id))

    async def add_record(self, table: str, data: dict):
        return await self.__client.create(table, data)

    async def add_relation(
            self,
            table: str,
            data_table: str,
            source: str,
            target: str,
            relation_type: int = 0,
            data: dict = None
    ):
        if data is None:
            data = {}
        return await self.__client.insert_relation(table, {
            "in": RecordID(data_table, source),
            "out": RecordID(data_table, target),
            "relation_type": relation_type,
            "data": data
        })
