from core.api import Api
from infra import Config, Db, Data

class CoreService:
    def __init__(self):
        self.__config = Config()
        self.__db = Db(self.__config)
        self.__data = Data(self.__config)
        self.api = Api(self.__db, self.__data)

    async def start(self):
        """启动服务"""
        await self.__db.start()
        await self.__data.start()

    async def stop(self):
        """关闭服务"""
        await self.__db.stop()
        await self.__data.stop()

