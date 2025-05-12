import os
from datetime import timedelta
from io import BytesIO

from common import FileInfo
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

    def __upload_object(self, file: FileInfo, data: bytes):
        self.__client.put_object(self.__bucket, file.id, BytesIO(data), len(data), content_type=file.content_type)

    async def upload_object(self, file: FileInfo, data: bytes):
        """
        上传对象
        :param file: 文件数据
        :param data: 对象数据
        """
        self.__upload_object(file, data)

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
