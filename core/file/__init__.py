import logging

from infra import Db, Data
from common import FileInfo, calculate_md5, init_dataclass_from_dict
from uuid import uuid4
from datetime import datetime


class FileService:
    def __init__(self, db: Db, data: Data):
        self.__db = db
        self.__data = data
        self.__table_file = 'file'

    async def add_file(self, file_name: str, data: bytes) -> str:
        """
        创建一个文件
        :param file_name: 文件名称
        :param data: 文件数据
        :return:
        """
        file = FileInfo(
            id=uuid4().hex,
            name=file_name,
            size=len(data),
            md5=calculate_md5(data),
            create_time=datetime.now()
        )
        logging.info(f"file {file.id} name {file.name} md5 {file.md5}")
        # 上传文件
        await self.__data.upload_object(file_name, file.id, data)
        # 添加一条记录
        await self.__db.add_record(self.__table_file, file.__dict__)
        return file.id

    async def __get_file_info(self, file_id: str) -> FileInfo:
        file = await self.__db.select_id(self.__table_file, file_id)
        if file is None:
            raise Exception('file not found')
        return init_dataclass_from_dict(FileInfo, file)

    async def get_file(self, file_id: str) -> (FileInfo, bytes):
        """
        获取文件数据
        :param file_id: 文件id
        :return:
        """
        return self.__get_file_info(file_id), await self.__data.get_object_bytes(file_id)

    async def get_file_link(self, file_id: str) -> (FileInfo, bytes):
        """
        获取文件下载链接
        :param file_id: 文件id
        :return:
        """
        return await self.__get_file_info(file_id), self.__data.get_object_link(file_id)
