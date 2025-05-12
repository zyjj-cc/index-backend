import logging
import os

from infra import Db, Data
from common import FileInfo, calculate_md5, init_dataclass_from_dict, get_datetime_now
from uuid import uuid4


class FileService:
    def __init__(self, db: Db, data: Data):
        self.__db = db
        self.__data = data
        self.__table_file = 'file'

    @staticmethod
    def __get_content_type(file_name: str):
        content_type_mapping = {
            '.html': 'text/html',
            '.htm': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.txt': 'text/plain',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.pdf': 'application/pdf',
        }
        file_extension = os.path.splitext(file_name)[1].lower()
        return content_type_mapping.get(file_extension, 'application/octet-stream')

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
            content_type=self.__get_content_type(file_name),
            size=len(data),
            md5=calculate_md5(data),
            create_time=get_datetime_now()
        )
        logging.info(f"file {file.id} name {file.name} md5 {file.md5}")
        # 上传文件
        await self.__data.upload_object(file, data)
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
        return await self.__get_file_info(file_id), await self.__data.get_object_bytes(file_id)

    async def get_file_link(self, file_id: str) -> (FileInfo, bytes):
        """
        获取文件下载链接
        :param file_id: 文件id
        :return:
        """
        return await self.__get_file_info(file_id), self.__data.get_object_link(file_id)
