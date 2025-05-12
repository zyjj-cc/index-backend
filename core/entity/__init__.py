import logging

from core.entity.trigger import Trigger
from infra import Db
from common import EntityInfo, EntityRelation, init_dataclass_from_dict, get_datetime_now
from uuid import uuid4
from datetime import datetime

class EntityService:
    def __init__(self, db: Db):
        self.__db = db
        self.__table_entity = 'entity'
        self.__table_entity_relation = 'entity_relation'
        self.__trigger = Trigger()

    async def add_entity(self, entity: EntityInfo) -> str:
        """
        添加一个实体
        :param entity: 实体信息
        :return:
        """
        if not entity.data:
            entity.data = {}
        entity.id = uuid4().hex
        entity.create_time = get_datetime_now()
        entity.update_time = get_datetime_now()
        logging.info(f"entity info {entity.__dict__}")
        await self.__db.add_record(self.__table_entity, entity.__dict__)
        return entity.id

    async def get_entity(self, entity_id: str) -> EntityInfo:
        """
        获取实体信息
        :param entity_id: 实体id
        :return:
        """
        data = await self.__db.select_id(self.__table_entity, entity_id)
        logging.info(f"entity data {data}")
        return init_dataclass_from_dict(EntityInfo, data)

    async def update_entity(self, entity_id: str, name: str = '', data: dict = None):
        """
        实体更新
        :param entity_id: 实体id
        :param name: 实体名称
        :param data: 实体数据
        :return:
        """
        update = [{"op": 'replace', "path": '/update_time', "value": datetime.now()}]
        if name:
            update.append({"op": 'replace', "path": '/name', "value": name})
        if data is not None:
            update.append({"op": 'replace', "path": '/data', "value": data})
        await self.__db.patch_record(self.__table_entity, entity_id, update)

    async def delete_entity(self, entity_id: str):
        """
        删除实体
        :param entity_id: 实体id
        :return:
        """
        await self.__db.delete_record(self.__table_entity, entity_id)

    async def add_relation(self, relation: EntityRelation):
        """
        添加一个关联
        :param relation: 关联信息
        :return:
        """
        if not relation.data:
            relation.data = {}

        await self.__db.add_relation(
            self.__table_entity_relation,
            self.__table_entity,
            relation.source,
            relation.target,
            {
                "relation_type": relation.relation_type,
                "data": relation.data,
                "create_time": get_datetime_now()
            }
        )

    async def get_relation_target(self, entity_id: str):
        """
        添加一个关联
        :param entity_id: 实体id
        :return:
        """
        data = await self.__db.query_data(
            f"SELECT out.id as id, out.name as name, relation_type FROM {self.__table_entity_relation} "
            f"WHERE in.id = {self.__table_entity}:{entity_id};"
        )
        for record in data:
            record["id"] = record["id"].id
        return data

    async def get_all_relation(self, relation_type: int):
        """
        获取所有联系
        :param relation_type: 联系类型
        :return:
        """
        condition = []
        if relation_type is not None:
            condition.append(f"relation_type={relation_type}")
        sql = f"SELECT in.id, in.entity_type, in.name ,out.id, out.entity_type, out.name, relation_type " \
              f"FROM {self.__table_entity_relation} "
        if condition:
            sql += f"WHERE {' AND '.join(condition)}"

        data = await self.__db.query_data(sql)
        for record in data:
            record["in"]["id"] = record["in"]["id"].id
            record["out"]["id"] = record["out"]["id"].id
        return data

    async def entity_trigger(self, entity_id: str, data: dict) -> dict:
        entity_info = await self.get_entity(entity_id)
        return await self.__trigger.entity_trigger(entity_info, data)



