import logging

from infra import Db
from common import EntityInfo, init_dataclass_from_dict
from uuid import uuid4
from datetime import datetime

class EntityService:
    def __init__(self, db: Db):
        self.__db = db
        self.__table_entity = 'entity'

    async def add_entity(self, entity: EntityInfo):
        """
        添加一个实体
        :param entity: 实体信息
        :return:
        """
        if not entity.data:
            entity.data = {}
        entity.id = uuid4().hex
        entity.create_time = datetime.now()
        logging.info(f"entity info {entity.__dict__}")
        await self.__db.add_record(self.__table_entity, entity.__dict__)

    async def get_entity(self, record_id: str) -> EntityInfo:
        """
        获取一个实体
        :param record_id: 实体id
        :return:
        """
        data = await self.__db.select_id(self.__table_entity, record_id)
        return init_dataclass_from_dict(EntityInfo, data)

