import os
from datetime import timedelta
from io import BytesIO

from minio import Minio

from infra import Config


class Data:
    def __init__(self, config: Config):
        self.__client = Minio(
            config.data_endpoint,
            access_key=config.data_ak,
            secret_key=config.data_sk,
            secure=False
        )
        self.__bucket = config.data_bucket

    async def start(self):
        pass

    async def stop(self):
        pass

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

    def __upload_object(self, file_name: str, key: str, data: bytes):
        self.__client.put_object(self.__bucket, key, BytesIO(data), len(data), content_type=self.__get_content_type(file_name))

    async def upload_object(self, file_name: str, key: str, data: bytes):
        """
        上传对象
        :param file_name: 文件名称
        :param key: 文件key
        :param data: 对象数据
        """
        self.__upload_object(file_name, key, data)

    async def get_object_bytes(self, key: str):
        """
        获取某个对象的字节流
        :param key: 对象名称
        :return: 字节数据
        """
        return self.__client.get_object(self.__bucket, key).data

    def get_object_link(self, key: str):
        """
        获取某个对象的链接
        :param key: 对象名称
        :return: 链接
        """
        return self.__client.presigned_get_object(self.__bucket, key, timedelta(hours=3))
